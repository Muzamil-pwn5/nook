import os

from dotenv import load_dotenv

from app.llm.base import LLMProvider


load_dotenv()


def get_llm_provider() -> LLMProvider:
    """
    Create the configured LLM provider.

    Supported providers:
        - mock
        - groq
        - openai
        - gemini
    """

    provider_name = os.getenv("LLM_PROVIDER", "").strip().lower()

    if not provider_name:
        if os.getenv("GROQ_API_KEY"):
            provider_name = "groq"
        elif os.getenv("GEMINI_API_KEY"):
            provider_name = "gemini"
        else:
            raise RuntimeError(
                "No live LLM provider is configured. Set LLM_PROVIDER and its API key."
            )

    if provider_name == "groq":
        from app.llm.groq_provider import GroqProvider

        return GroqProvider()

    if provider_name == "gemini":
        from app.llm.gemini_provider import GeminiProvider

        return GeminiProvider()

    if provider_name == "openai":
        from app.llm.openai_provider import OpenAIProvider

        return OpenAIProvider()

    if provider_name == "mock":
        from app.llm.mock import MockLLMProvider

        return MockLLMProvider()

    raise ValueError(
        f"Unsupported LLM provider: {provider_name}. "
        "Supported providers are: mock, groq, openai, gemini."
    )
