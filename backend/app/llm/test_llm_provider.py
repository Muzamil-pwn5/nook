import os

from app.llm.mock import MockLLMProvider
from app.llm.provider_factory import get_llm_provider


def test_default_provider_requires_live_configuration(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        get_llm_provider()
    except RuntimeError as error:
        assert "No live LLM provider is configured" in str(error)
    else:
        raise AssertionError("Expected live provider configuration to be required.")


def test_explicit_mock_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    provider = get_llm_provider()

    assert isinstance(provider, MockLLMProvider)


def test_unsupported_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "unsupported")

    try:
        get_llm_provider()
    except ValueError as error:
        assert "Unsupported LLM provider" in str(error)
    else:
        raise AssertionError(
            "Expected unsupported provider to raise ValueError."
        )
