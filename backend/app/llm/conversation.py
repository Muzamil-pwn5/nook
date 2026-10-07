from dataclasses import dataclass, field


@dataclass
class ConversationMessage:
    """
    One message or tool-related event in an agent conversation.
    """

    role: str
    content: str = ""
    tool_call_id: str | None = None
    tool_name: str | None = None
    tool_arguments: dict | None = None


@dataclass
class AgentConversation:
    """
    Stores the complete conversation state required for
    multi-turn agent reasoning and tool execution.
    """

    messages: list[ConversationMessage] = field(
        default_factory=list
    )

    # Gemini Interactions API conversation state.
    #
    # This is intentionally stored inside the conversation
    # object rather than globally so different users/sessions
    # cannot accidentally share Gemini context.
    gemini_interaction_id: str | None = None

    def add_user_message(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            ConversationMessage(
                role="user",
                content=content,
            )
        )

    def add_assistant_message(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            ConversationMessage(
                role="assistant",
                content=content,
            )
        )

    def add_assistant_tool_call(
        self,
        tool_call_id: str,
        tool_name: str,
        arguments: dict,
    ) -> None:
        """
        Record a tool call requested by the model.
        """

        self.messages.append(
            ConversationMessage(
                role="assistant_tool_call",
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                tool_arguments=arguments,
            )
        )

    def add_tool_result(
        self,
        tool_call_id: str,
        tool_name: str,
        content: str,
    ) -> None:
        """
        Record the result returned by an executed tool.
        """

        self.messages.append(
            ConversationMessage(
                role="tool",
                content=content,
                tool_call_id=tool_call_id,
                tool_name=tool_name,
            )
        )