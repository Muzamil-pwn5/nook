from types import SimpleNamespace

from app.llm.openai_provider import OpenAIProvider
from app.llm.response import LLMResponse


def test_openai_response_normalization():
    function_call = SimpleNamespace(
        type="function_call",
        call_id="call_123",
        name="search_products",
        arguments='{"query":"laptop","category":"Laptops","max_price":650}',
    )

    message_output = SimpleNamespace(
        type="message",
    )

    fake_response = SimpleNamespace(
        output=[
            message_output,
            function_call,
        ],
        output_text="I found a laptop within your budget.",
    )

    result = OpenAIProvider._normalize_response(
        fake_response
    )

    assert isinstance(result, LLMResponse)

    assert result.text == (
        "I found a laptop within your budget."
    )

    assert len(result.tool_calls) == 1

    tool_call = result.tool_calls[0]

    assert tool_call["call_id"] == "call_123"
    assert tool_call["tool_name"] == "search_products"

    assert tool_call["arguments"] == {
        "query": "laptop",
        "category": "Laptops",
        "max_price": 650,
    }


def test_openai_response_without_tool_calls():
    fake_response = SimpleNamespace(
        output=[],
        output_text="I can help you find a product.",
    )

    result = OpenAIProvider._normalize_response(
        fake_response
    )

    assert isinstance(result, LLMResponse)
    assert result.text == "I can help you find a product."
    assert result.tool_calls == []