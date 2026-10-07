import pytest
from fastapi.testclient import TestClient

import app.api.agent as agent_api
from app.llm.agent_runner import LLMAgentRunner
from app.llm.mock import MockLLMProvider
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def use_deterministic_provider(monkeypatch):
    """Keep endpoint integration tests offline and deterministic."""
    monkeypatch.setattr(
        agent_api,
        "llm_agent",
        LLMAgentRunner(provider=MockLLMProvider()),
    )


def create_session() -> str:
    response = client.post("/agent/session")
    assert response.status_code == 200
    return response.json()["session_id"]


def test_chat_endpoint_completes_conversational_product_search():
    session_id = create_session()

    response = client.post(
        "/agent/chat",
        json={
            "session_id": session_id,
            "message": "I need a laptop under $650.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["agent"] == "llm"
    assert data["success"] is True
    assert data["type"] == "final_response"
    assert "HP Pavilion 14" in data["response"]
    assert "in stock" in data["response"].lower()
    assert data["session_id"] == session_id
    assert "conversation" not in data

    follow_up = client.post(
        "/agent/chat",
        json={
            "session_id": session_id,
            "message": "Can you say that more simply?",
        },
    )

    assert follow_up.status_code == 200
    assert "conversation" not in follow_up.json()
    assert len(agent_api.sessions[session_id]["conversation"].messages) == 8


def test_chat_endpoint_returns_approval_request_for_order():
    session_id = create_session()

    response = client.post(
        "/agent/chat",
        json={
            "session_id": session_id,
            "message": "I want to buy the laptop.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["agent"] == "llm"
    assert data["success"] is False
    assert data["type"] == "approval_required"
    assert data["approval_id"]
    assert data["pending_action"]["tool_name"] == "create_order"


def test_chat_endpoint_rejects_unknown_session():
    response = client.post(
        "/agent/chat",
        json={
            "session_id": "missing-session",
            "message": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found."}
