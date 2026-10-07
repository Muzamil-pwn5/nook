from app.agents.orchestrator import AgentOrchestrator
from app.llm.tool_call import ToolCall
from app.llm.tool_executor import LLMToolExecutor


def test_llm_can_execute_low_risk_tool():
    executor = LLMToolExecutor()

    tool_call = ToolCall(
        call_id="test-call-1",
        tool_name="check_inventory",
        arguments={
            "product_id": 1,
        },
    )

    result = executor.execute(tool_call)

    assert result["success"] is True
    assert result["tool"] == "check_inventory"
    assert result["result"]["success"] is True


def test_llm_cannot_execute_order_without_approval():
    executor = LLMToolExecutor()

    tool_call = ToolCall(
        call_id="test-call-2",
        tool_name="create_order",
        arguments={
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "product_id": 2,
            "quantity": 1,
        },
    )

    result = executor.execute(tool_call)

    assert result["success"] is False
    assert result["requires_approval"] is True


def test_llm_cannot_execute_unknown_tool():
    executor = LLMToolExecutor()

    tool_call = ToolCall(
        call_id="test-call-3",
        tool_name="delete_database",
        arguments={},
    )

    result = executor.execute(tool_call)

    assert result["success"] is False
    assert "not available" in result["error"]


def test_executor_uses_supplied_orchestrator():
    orchestrator = AgentOrchestrator()
    executor = LLMToolExecutor(orchestrator=orchestrator)

    assert executor.orchestrator is orchestrator