import json
import os
from typing import Any

from openai import OpenAI

from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse
from app.llm.tool_schemas import get_tool_schemas


class OpenAIProvider(LLMProvider):
    """
    OpenAI LLM provider.

    This provider handles communication with the model only.
    Business tools are executed by the application's orchestrator.
    """

    def __init__(
        self,
        model: str | None = None,
    ):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

        self.model = model or os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6",
        )

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        """
        Return the tools exposed to the model.
        """
        return get_tool_schemas()

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        """
        Generate the next model response using the complete
        agent conversation.
        """

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=self._build_input(conversation),
            tools=self.get_tool_schemas(),
        )

        return self._normalize_response(response)

    @staticmethod
    def _build_input(
        conversation: AgentConversation,
    ) -> list[dict[str, Any]]:
        """
        Convert our internal conversation representation into
        Responses API input items.

        Important:
        - User messages become user input.
        - Assistant tool calls become function_call items.
        - Tool results become function_call_output items.
        - Normal assistant text becomes assistant content.
        """

        input_items: list[dict[str, Any]] = []

        for message in conversation.messages:

            if message.role == "user":
                input_items.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": message.content,
                            }
                        ],
                    }
                )

            elif message.role == "assistant":
                if not message.content:
                    continue

                input_items.append(
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "output_text",
                                "text": message.content,
                            }
                        ],
                    }
                )

            elif message.role == "assistant_tool_call":
                if not message.tool_call_id:
                    continue

                input_items.append(
                    {
                        "type": "function_call",
                        "call_id": message.tool_call_id,
                        "name": message.tool_name,
                        "arguments": json.dumps(
                            message.tool_arguments or {}
                        ),
                    }
                )

            elif message.role == "tool":
                if not message.tool_call_id:
                    continue

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": message.tool_call_id,
                        "output": message.content,
                    }
                )

        return input_items

    @staticmethod
    def _normalize_response(response) -> LLMResponse:
        """
        Convert the provider-specific OpenAI response into
        our provider-independent LLMResponse.
        """

        tool_calls: list[dict[str, Any]] = []

        for item in response.output:
            if item.type != "function_call":
                continue

            tool_calls.append(
                {
                    "call_id": item.call_id,
                    "tool_name": item.name,
                    "arguments": json.loads(item.arguments),
                }
            )

        return LLMResponse(
            text=response.output_text or "",
            tool_calls=tool_calls,
            raw_response=response,
        )
