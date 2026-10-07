from app.agents.orchestrator import AgentOrchestrator
from app.llm.agent_runner import LLMAgentRunner
from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse
from app.llm.tool_executor import LLMToolExecutor
from app.llm.tool_loop import LLMToolLoop


class SimulatedAgentProvider(LLMProvider):
    """
    Deterministic simulated LLM.

    Simulates a model that performs multiple reasoning steps
    and requests tools before producing a final response.
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
                        "call_id": "search_1",
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
                        "call_id": "inventory_1",
                        "tool_name": "check_inventory",
                        "arguments": {
                            "product_id": 2,
                        },
                    }
                ]
            )

        return LLMResponse(
            text=(
                "I found the HP Pavilion 14 for $649.99 "
                "and confirmed that it is currently in stock."
            )
        )


class NeverEndingToolProvider(LLMProvider):
    """
    Simulates a model that never produces a final response.

    Used to verify that the runner's iteration limit prevents
    an infinite agent loop.
    """

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:
        return LLMResponse(
            tool_calls=[
                {
                    "call_id": "search_loop",
                    "tool_name": "search_products",
                    "arguments": {
                        "query": "laptop",
                        "category": None,
                        "max_price": 650,
                    },
                }
            ]
        )


def test_llm_agent_runner_complete_workflow():
    provider = SimulatedAgentProvider()

    orchestrator = AgentOrchestrator()

    tool_executor = LLMToolExecutor(
        orchestrator=orchestrator
    )

    tool_loop = LLMToolLoop(
        tool_executor=tool_executor
    )

    runner = LLMAgentRunner(
        provider=provider,
        tool_loop=tool_loop,
        max_iterations=5,
    )

    result = runner.run(
        "Find me a laptop under $650."
    )

    assert result["success"] is True
    assert result["type"] == "final_response"

    assert "HP Pavilion 14" in result["response"]
    assert "in stock" in result["response"].lower()

    assert result["iterations"] == 3

    conversation = result["conversation"]

    assert len(conversation.messages) == 6

    assert conversation.messages[0].role == "user"
    assert conversation.messages[1].role == "assistant_tool_call"
    assert conversation.messages[2].role == "tool"
    assert conversation.messages[3].role == "assistant_tool_call"
    assert conversation.messages[4].role == "tool"
    assert conversation.messages[5].role == "assistant"

    assert provider.call_count == 3


def test_llm_agent_runner_iteration_limit():
    provider = NeverEndingToolProvider()

    runner = LLMAgentRunner(
        provider=provider,
        max_iterations=3,
    )

    result = runner.run(
        "Find me a laptop under $650."
    )

    assert result["success"] is False
    assert result["type"] == "iteration_limit"
    assert result["iterations"] == 3

    assert (
        "allowed number of reasoning steps"
        in result["response"]
    )

    assert len(result["conversation"].messages) == 7