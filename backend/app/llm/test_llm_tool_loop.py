from app.llm.response import LLMResponse
from app.llm.tool_loop import LLMToolLoop


def test_tool_loop_executes_safe_tool():
    response = LLMResponse(
        text="Checking inventory.",
        tool_calls=[
            {
                "call_id": "call-1",
                "tool_name": "check_inventory",
                "arguments": {
                    "product_id": 1,
                },
            }
        ],
    )

    loop = LLMToolLoop()

    results = loop.execute_response(response)

    assert len(results) == 1
    assert results[0]["call_id"] == "call-1"
    assert results[0]["tool_name"] == "check_inventory"
    assert results[0]["result"]["success"] is True


def test_tool_loop_enforces_order_approval():
    response = LLMResponse(
        text="Preparing the order.",
        tool_calls=[
            {
                "call_id": "call-2",
                "tool_name": "create_order",
                "arguments": {
                    "customer_name": "Test User",
                    "customer_email": "test@example.com",
                    "product_id": 2,
                    "quantity": 1,
                },
            }
        ],
    )

    loop = LLMToolLoop()

    results = loop.execute_response(response)

    assert len(results) == 1

    result = results[0]["result"]

    assert result["success"] is False
    assert result["requires_approval"] is True