from dataclasses import dataclass


@dataclass
class ToolCall:
    """
    Represents a tool call requested by an LLM.

    The LLM only proposes the action.
    The orchestrator remains responsible for execution,
    permissions, validation, and auditing.
    """

    call_id: str
    tool_name: str
    arguments: dict