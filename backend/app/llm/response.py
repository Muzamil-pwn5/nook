from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    """
    Normalized response returned by an LLM provider.

    Providers may use completely different SDK response formats,
    but the rest of our application should work with this common
    representation.
    """

    text: str = ""
    tool_calls: list[dict] = field(default_factory=list)
    raw_response: object | None = None