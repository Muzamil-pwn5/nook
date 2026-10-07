import json
import os

from dotenv import load_dotenv
from google import genai

from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse


load_dotenv()


class GeminiProvider(LLMProvider):
    """
    Gemini LLM provider using Google's current Interactions API.

    Gemini decides WHAT action should happen.

    Our application still controls:
        - whether the tool exists
        - whether the action is permitted
        - whether approval is required
        - actual tool execution
        - database access

    Gemini never accesses the database directly.
    """

    def __init__(self, model: str | None = None):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = (
            model
            or os.getenv(
                "GEMINI_MODEL",
                "gemini-3.1-flash-lite",
            )
        )

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        """
        Generate the next model response.

        We use Google's stateful Interactions API.

        The conversation object stores the latest Gemini
        interaction ID so subsequent tool results can be
        attached to the correct model turn.
        """

        tools = self._build_tools()

        interaction_id = getattr(
            conversation,
            "gemini_interaction_id",
            None,
        )

        if interaction_id:
            interaction = self.client.interactions.create(
                model=self.model,
                previous_interaction_id=interaction_id,
                input=self._build_follow_up_input(
                    conversation
                ),
                system_instruction=system_prompt,
                tools=tools,
            )

        else:
            interaction = self.client.interactions.create(
                model=self.model,
                input=self._build_initial_input(
                    conversation
                ),
                system_instruction=system_prompt,
                tools=tools,
            )

        conversation.gemini_interaction_id = (
            interaction.id
        )

        return self._convert_response(
            interaction
        )

    def _build_initial_input(
        self,
        conversation: AgentConversation,
    ) -> str:
        """
        Extract the first user message.

        The Interactions API stores the conversation
        state server-side, so we only need to send the
        current user input when starting a conversation.
        """

        for message in conversation.messages:
            if message.role == "user":
                return message.content

        return ""

    def _build_follow_up_input(
        self,
        conversation: AgentConversation,
    ) -> list[dict]:
        """
        Build the next input for Gemini.

        After a function call, send the executed tool
        result back as a function_result step.

        For ordinary user follow-ups, send the newest
        user message.
        """

        tool_results = [
            message
            for message in conversation.messages
            if message.role == "tool"
        ]

        if tool_results:
            latest_tool_result = tool_results[-1]

            result = self._parse_tool_result(
                latest_tool_result.content
            )

            return [
                {
                    "type": "function_result",
                    "name": (
                        latest_tool_result.tool_name
                        or ""
                    ),
                    "call_id": (
                        latest_tool_result.tool_call_id
                        or ""
                    ),
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                result,
                                default=str,
                            ),
                        }
                    ],
                }
            ]

        user_messages = [
            message
            for message in conversation.messages
            if message.role == "user"
        ]

        if user_messages:
            return user_messages[-1].content

        return ""

    def _convert_response(
        self,
        interaction,
    ) -> LLMResponse:
        """
        Convert Gemini's Interaction response into
        our application's provider-neutral LLMResponse.
        """

        tool_calls = []

        for step in getattr(
            interaction,
            "steps",
            [],
        ):
            if getattr(
                step,
                "type",
                None,
            ) != "function_call":
                continue

            arguments = getattr(
                step,
                "arguments",
                {},
            )

            if arguments is None:
                arguments = {}

            tool_calls.append(
                {
                    "call_id": (
                        getattr(
                            step,
                            "id",
                            None,
                        )
                        or ""
                    ),
                    "tool_name": (
                        getattr(
                            step,
                            "name",
                            None,
                        )
                        or ""
                    ),
                    "arguments": dict(
                        arguments
                    ),
                }
            )

        if tool_calls:
            return LLMResponse(
                tool_calls=tool_calls,
                raw_response=interaction,
            )

        return LLMResponse(
            text=(
                getattr(
                    interaction,
                    "output_text",
                    None,
                )
                or ""
            ),
            raw_response=interaction,
        )

    def _build_tools(self) -> list[dict]:
        """
        Convert our internal tool schemas into the format
        expected by Gemini Interactions API.
        """

        from app.llm.tool_schemas import (
            get_tool_schemas,
        )

        tools = []

        for schema in get_tool_schemas():
            if schema.get("type") != "function":
                continue

            tools.append(
                {
                    "type": "function",
                    "name": schema["name"],
                    "description": schema[
                        "description"
                    ],
                    "parameters": self._normalize_schema(
                        schema["parameters"]
                    ),
                }
            )

        return tools

    def _normalize_schema(
        self,
        schema: dict,
    ) -> dict:
        """
        Normalize our OpenAI-style JSON schemas into
        Gemini-compatible function declaration schemas.

        Gemini's current Interactions API accepts ordinary
        JSON-schema-style parameter definitions.
        """

        normalized = dict(schema)

        properties = normalized.get(
            "properties",
            {},
        )

        normalized_properties = {}

        for name, property_schema in properties.items():
            normalized_property = dict(
                property_schema
            )

            property_type = normalized_property.get(
                "type"
            )

            if isinstance(
                property_type,
                list,
            ):
                non_null_types = [
                    value
                    for value in property_type
                    if value != "null"
                ]

                if len(non_null_types) == 1:
                    normalized_property[
                        "type"
                    ] = non_null_types[0]

            normalized_property.pop(
                "nullable",
                None,
            )

            normalized_properties[name] = (
                normalized_property
            )

        normalized[
            "properties"
        ] = normalized_properties

        normalized.pop(
            "additionalProperties",
            None,
        )

        normalized.pop(
            "strict",
            None,
        )

        return normalized

    def _parse_tool_result(
        self,
        content: str,
    ) -> dict:
        """
        Convert our tool result string back into a
        structured result for Gemini.
        """

        try:
            parsed = json.loads(content)

            if isinstance(parsed, dict):
                return parsed

            return {
                "result": parsed
            }

        except json.JSONDecodeError:
            return {
                "result": content
            }
