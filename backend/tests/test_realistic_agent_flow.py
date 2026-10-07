from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse
from app.llm.tool_executor import LLMToolExecutor
from app.llm.tool_loop import LLMToolLoop


class SimulatedAgentProvider(LLMProvider):
    """
    Deterministic model simulator.

    It behaves like an LLM that reasons through multiple
    tool calls, allowing us to test the real agent architecture
    without an API key.
    """

    def __init__(self):
        self.call_count = 0

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        self.call_count += 1

        if self.call_count == 1:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "call_search_1",
                        "tool_name": "search_products",
                        "arguments": {
                            "query": "laptop",
                            "category": None,
                            "max_price": 650,
                        },
                    }
                ]
            )

        if self.call_count == 2:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "call_inventory_1",
                        "tool_name": "check_inventory",
                        "arguments": {
                            "product_id": 2,
                        },
                    }
                ]
            )

        return LLMResponse(
            text=(
                "I found the HP Pavilion 14 within your budget "
                "and confirmed that it is currently in stock."
            )
        )


def test_multi_step_agent_tool_flow():
    provider = SimulatedAgentProvider()
    tool_loop = LLMToolLoop(
        tool_executor=LLMToolExecutor()
    )

    conversation = AgentConversation()

    conversation.add_user_message(
        "Find me a laptop under $650."
    )

    # Step 1: model requests product search.
    response = provider.generate(
        system_prompt="Test system prompt",
        conversation=conversation,
    )

    assert len(response.tool_calls) == 1
    assert response.tool_calls[0]["tool_name"] == "search_products"

    for tool_call in response.tool_calls:
        conversation.add_assistant_tool_call(
            tool_call_id=tool_call["call_id"],
            tool_name=tool_call["tool_name"],
            arguments=tool_call["arguments"],
        )

    results = tool_loop.execute_response(response)

    assert results[0]["result"]["success"] is True

    conversation.add_tool_result(
        tool_call_id=results[0]["call_id"],
        tool_name=results[0]["tool_name"],
        content=str(results[0]["result"]),
    )

    # Step 2: model requests inventory verification.
    response = provider.generate(
        system_prompt="Test system prompt",
        conversation=conversation,
    )

    assert len(response.tool_calls) == 1
    assert response.tool_calls[0]["tool_name"] == "check_inventory"

    for tool_call in response.tool_calls:
        conversation.add_assistant_tool_call(
            tool_call_id=tool_call["call_id"],
            tool_name=tool_call["tool_name"],
            arguments=tool_call["arguments"],
        )

    results = tool_loop.execute_response(response)

    assert results[0]["result"]["success"] is True
    assert results[0]["result"]["result"]["product_id"] == 2

    conversation.add_tool_result(
        tool_call_id=results[0]["call_id"],
        tool_name=results[0]["tool_name"],
        content=str(results[0]["result"]),
    )

    # Step 3: model produces its final answer.
    response = provider.generate(
        system_prompt="Test system prompt",
        conversation=conversation,
    )

    assert response.tool_calls == []
    assert "HP Pavilion 14" in response.text
    assert "in stock" in response.text.lower()

    # Verify that the complete conversation was preserved.
    assert len(conversation.messages) == 5