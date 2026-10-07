from app.agents.customer_agent_runner import CustomerAgentRunner
from app.agents.customer_operations import CustomerOperationsAgent
from app.agents.decision_engine import CustomerDecisionEngine
from app.agents.conversation_state import ConversationState
from app.agents.orchestrator import AgentOrchestrator


def test_product_search():
    runner = CustomerAgentRunner()

    result = runner.handle_message(
        "I need a laptop under $650"
    )

    assert result["success"] is True
    assert result["tool"] == "search_products"
    assert result["state"]["selected_product_id"] == 2
    assert result["state"]["search_result_count"] == 1


def test_conversation_remembers_selected_product():
    state = ConversationState()

    state.remember_products(
        [
            {
                "id": 2,
                "name": "HP Pavilion 14",
                "price": 649.99,
            }
        ]
    )

    assert state.selected_product_id == 2

    product = state.get_selected_product()

    assert product is not None
    assert product["name"] == "HP Pavilion 14"


def test_buy_that_one_uses_previous_product():
    state = ConversationState()
    state.selected_product_id = 2

    engine = CustomerDecisionEngine()

    decision = engine.decide(
        "Buy that one",
        state,
    )

    assert decision.intent == "create_order"
    assert decision.tool_name == "create_order"
    assert decision.arguments["product_id"] == 2
    assert decision.arguments["quantity"] == 1


def test_missing_customer_information_creates_pending_action():
    runner = CustomerAgentRunner()

    runner.handle_message(
        "I need a laptop under $650"
    )

    result = runner.handle_message(
        "Buy that one"
    )

    assert result["success"] is False
    assert result["type"] == "customer_information_required"
    assert runner.state.pending_action == "create_order"
    assert runner.state.pending_arguments["product_id"] == 2


def test_order_requires_approval():
    agent = CustomerOperationsAgent()

    result = agent.create_order(
        customer_name="Test User",
        customer_email="test@example.com",
        product_id=2,
        quantity=1,
        approved=False,
    )

    assert result["success"] is False
    assert result["requires_approval"] is True


def test_unknown_tool_is_blocked():
    orchestrator = AgentOrchestrator()

    result = orchestrator.execute_tool(
        tool_name="delete_database",
        arguments={},
    )

    assert result["success"] is False
    assert "not available" in result["error"]