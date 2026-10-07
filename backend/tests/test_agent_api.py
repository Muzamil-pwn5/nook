import pytest

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
import app.api.agent as agent_api
from app.api.agent import sessions
from app.database.connection import engine
from app.database.models import (
    Customer,
    Order,
    OrderItem,
    Product,
)
from app.llm.agent_runner import LLMAgentRunner
from app.llm.mock import MockLLMProvider


client = TestClient(app)


@pytest.fixture(autouse=True)
def use_mock_llm_provider(monkeypatch):
    """
    Force API tests to use the deterministic mock provider.

    Production remains configured for Gemini through .env.
    """

    monkeypatch.setattr(
        agent_api,
        "llm_agent",
        LLMAgentRunner(
            provider=MockLLMProvider()
        ),
    )


def create_session() -> str:

    response = client.post(
        "/agent/session"
    )

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data

    return data["session_id"]


def get_product(
    product_id: int,
) -> Product:

    with Session(engine) as session:

        product = session.get(
            Product,
            product_id,
        )

        if product is None:
            raise AssertionError(
                f"Product {product_id} was not found."
            )

        session.expunge(product)

        return product


def get_latest_order_for_email(
    email: str,
) -> Order | None:

    with Session(engine) as session:

        customer = (
            session.query(Customer)
            .filter(
                Customer.email == email
            )
            .first()
        )

        if customer is None:
            return None

        order = (
            session.query(Order)
            .filter(
                Order.customer_id == customer.id
            )
            .order_by(Order.id.desc())
            .first()
        )

        if order is None:
            return None

        session.expunge(order)

        return order


def delete_order(
    order_id: int,
) -> None:

    with Session(engine) as session:

        order_items = (
            session.query(OrderItem)
            .filter(
                OrderItem.order_id == order_id
            )
            .all()
        )

        for item in order_items:
            session.delete(item)

        order = session.get(
            Order,
            order_id,
        )

        if order is not None:
            session.delete(order)

        session.commit()


def test_complete_order_flow_with_approval():

    """
    Tests:

        session creation
        -> agent request
        -> approval required
        -> approval ID
        -> human approval
        -> real database order
        -> inventory decrease
    """

    product_id = 2

    customer_email = (
        "ahmed.test@example.com"
    )

    session_id = create_session()

    product_before = get_product(
        product_id
    )

    stock_before = (
        product_before.stock_quantity
    )

    latest_order_before = (
        get_latest_order_for_email(
            customer_email
        )
    )

    previous_order_id = (
        latest_order_before.id
        if latest_order_before is not None
        else None
    )

    response = client.post(
        "/agent/chat",
        json={
            "session_id": session_id,
            "message": (
                "I want to buy the HP Pavilion 14. "
                "My name is Ahmed Khan and my email "
                "is ahmed.test@example.com. "
                "Quantity 1."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["agent"] == "llm"
    assert data["success"] is False
    assert data["type"] == "approval_required"
    assert data["session_id"] == session_id

    assert "approval_id" in data

    approval_id = data["approval_id"]

    assert approval_id

    assert approval_id in (
        sessions[session_id][
            "pending_approvals"
        ]
    )

    assert (
        data["pending_action"]["tool_name"]
        == "create_order"
    )

    arguments = data[
        "pending_action"
    ]["arguments"]

    assert (
        arguments["customer_name"]
        == "Ahmed Khan"
    )

    assert (
        arguments["customer_email"]
        == customer_email
    )

    assert arguments["product_id"] == 2
    assert arguments["quantity"] == 1

    # Approval must NOT create the order.
    product_after_request = get_product(
        product_id
    )

    assert (
        product_after_request.stock_quantity
        == stock_before
    )

    # Approve the exact session + approval ID.
    approval_response = client.post(
        (
            f"/agent/session/{session_id}"
            f"/approve-order/{approval_id}"
        )
    )

    assert approval_response.status_code == 200

    approval_data = (
        approval_response.json()
    )

    assert approval_data["agent"] == "llm"
    assert approval_data["success"] is True

    assert (
        approval_data["type"]
        == "final_response"
    )

    assert (
        approval_data["response"]
        == (
            "Your order has been successfully "
            "created after approval."
        )
    )

    # Approval must be consumed.
    assert approval_id not in (
        sessions[session_id][
            "pending_approvals"
        ]
    )

    # Verify actual database order.
    latest_order = (
        get_latest_order_for_email(
            customer_email
        )
    )

    assert latest_order is not None

    new_order_id = latest_order.id

    if previous_order_id is not None:

        assert (
            new_order_id
            > previous_order_id
        )

    assert latest_order.status == "confirmed"

    assert float(
        latest_order.total_amount
    ) == 649.99

    # Verify actual inventory mutation.
    product_after_order = get_product(
        product_id
    )

    assert (
        product_after_order.stock_quantity
        == stock_before - 1
    )

    # Restore test inventory.
    with Session(engine) as session:

        product = session.get(
            Product,
            product_id,
        )

        if product is not None:
            product.stock_quantity += 1

        session.commit()

    delete_order(
        new_order_id
    )

    sessions.pop(
        session_id,
        None,
    )


def test_unknown_session_is_rejected():

    response = client.post(
        "/agent/chat",
        json={
            "session_id": (
                "00000000-0000-0000-0000-"
                "000000000000"
            ),
            "message": "Hello",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Session not found."
    )


def test_approval_belongs_to_correct_session():

    session_a = create_session()
    session_b = create_session()

    response = client.post(
        "/agent/chat",
        json={
            "session_id": session_a,
            "message": (
                "I want to buy the HP Pavilion 14. "
                "My name is Ahmed Khan and my email "
                "is ahmed.test@example.com. "
                "Quantity 1."
            ),
        },
    )

    assert response.status_code == 200

    approval_id = response.json()[
        "approval_id"
    ]

    # Session B must NOT be able to approve
    # Session A's action.
    wrong_session_response = client.post(
        (
            f"/agent/session/{session_b}"
            f"/approve-order/{approval_id}"
        )
    )

    assert (
        wrong_session_response.status_code
        == 404
    )

    # The approval must still belong to A.
    assert approval_id in (
        sessions[session_a][
            "pending_approvals"
        ]
    )

    # Clean up.
    sessions.pop(
        session_a,
        None,
    )

    sessions.pop(
        session_b,
        None,
    )


def test_invalid_approval_id_is_rejected():

    session_id = create_session()

    response = client.post(
        (
            f"/agent/session/{session_id}"
            "/approve-order/"
            "00000000-0000-0000-0000-"
            "000000000000"
        )
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == (
            "Approval request not found, "
            "expired, or already completed."
        )
    )

    sessions.pop(
        session_id,
        None,
    )