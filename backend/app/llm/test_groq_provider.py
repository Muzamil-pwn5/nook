from types import SimpleNamespace

from app.llm.conversation import AgentConversation
from app.llm.groq_provider import GroqProvider
from app.llm.response import LLMResponse


def test_groq_response_normalization():
    tool_call = SimpleNamespace(
        id="call_123",
        function=SimpleNamespace(
            name="search_products",
            arguments='{"query":"shirt","category":"Clothing","max_price":50}',
        ),
    )
    message = SimpleNamespace(
        content="I found a shirt for you.",
        tool_calls=[tool_call],
    )
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=message)],
    )

    result = GroqProvider._normalize_response(response)

    assert isinstance(result, LLMResponse)
    assert result.text == "I found a shirt for you."
    assert result.tool_calls == [
        {
            "call_id": "call_123",
            "tool_name": "search_products",
            "arguments": {
                "query": "shirt",
                "category": "Clothing",
                "max_price": 50,
            },
        }
    ]


def test_groq_builds_chat_completion_messages():
    conversation = AgentConversation()
    conversation.add_user_message("Find me a shirt.")
    conversation.add_assistant_tool_call(
        tool_call_id="call_1",
        tool_name="search_products",
        arguments={"query": "shirt", "category": None, "max_price": None},
    )
    conversation.add_tool_result(
        tool_call_id="call_1",
        tool_name="search_products",
        content='[{"id": 1}]',
    )

    messages = GroqProvider._build_messages("You are helpful.", conversation)

    assert messages[0] == {"role": "system", "content": "You are helpful."}
    assert messages[1] == {"role": "user", "content": "Find me a shirt."}
    assert messages[2]["role"] == "assistant"
    assert messages[2]["tool_calls"][0]["function"]["name"] == "search_products"
    assert messages[3] == {
        "role": "tool",
        "tool_call_id": "call_1",
        "content": '[{"id": 1}]',
    }


def test_groq_requires_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    try:
        GroqProvider()
    except RuntimeError as error:
        assert "GROQ_API_KEY is not configured" in str(error)
    else:
        raise AssertionError("Expected missing Groq key to be rejected.")
