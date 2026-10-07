import json
import os
from typing import Any

from openai import OpenAI

from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse
from app.llm.tool_schemas import get_tool_schemas


class GroqProvider(LLMProvider):
    """Groq provider using Groq's OpenAI-compatible Chat Completions API."""

    def __init__(self, model: str | None = None):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv(
                "GROQ_BASE_URL",
                "https://api.groq.com/openai/v1",
            ),
        )
        self.model = model or os.getenv(
            "GROQ_MODEL",
            "qwen/qwen3.8-27b",
        )

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(system_prompt, conversation),
            tools=self._build_tools(),
            tool_choice="auto",
        )
        return self._normalize_response(response)

    @staticmethod
    def _build_messages(
        system_prompt: str,
        conversation: AgentConversation,
    ) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]
        for message in conversation.messages:
            if message.role == "user":
                messages.append({"role": "user", "content": message.content})
            elif message.role == "assistant":
                messages.append({"role": "assistant", "content": message.content})
            elif message.role == "assistant_tool_call":
                messages.append(
                    {
                        "role": "assistant",
                        "content": message.content or None,
                        "tool_calls": [
                            {
                                "id": message.tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": message.tool_name,
                                    "arguments": json.dumps(
                                        message.tool_arguments or {}
                                    ),
                                },
                            }
                        ],
                    }
                )
            elif message.role == "tool":
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": message.tool_call_id,
                        "content": message.content,
                    }
                )
        return messages

    @staticmethod
    def _build_tools() -> list[dict[str, Any]]:
        tools = []
        for schema in get_tool_schemas():
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": schema["name"],
                        "description": schema["description"],
                        "parameters": schema["parameters"],
                    },
                }
            )
        return tools

    @staticmethod
    def _normalize_response(response) -> LLMResponse:
        message = response.choices[0].message
        tool_calls = []
        for tool_call in message.tool_calls or []:
            tool_calls.append(
                {
                    "call_id": tool_call.id,
                    "tool_name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments),
                }
            )
        return LLMResponse(
            text=message.content or "",
            tool_calls=tool_calls,
            raw_response=response,
        )
