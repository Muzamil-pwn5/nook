from app.llm.conversation import AgentConversation


def test_conversation_stores_user_and_assistant_messages():
    conversation = AgentConversation()

    conversation.add_user_message(
        "I need a laptop under $650."
    )

    conversation.add_assistant_message(
        "I found one laptop within your budget."
    )

    assert len(conversation.messages) == 2

    assert conversation.messages[0].role == "user"
    assert conversation.messages[0].content == (
        "I need a laptop under $650."
    )

    assert conversation.messages[1].role == "assistant"
    assert conversation.messages[1].content == (
        "I found one laptop within your budget."
    )


def test_conversation_stores_tool_result():
    conversation = AgentConversation()

    conversation.add_tool_result(
        tool_call_id="call-123",
        tool_name="check_inventory",
        content='{"stock_quantity": 11}',
    )

    assert len(conversation.messages) == 1

    message = conversation.messages[0]

    assert message.role == "tool"
    assert message.tool_call_id == "call-123"
    assert message.tool_name == "check_inventory"
    assert message.content == '{"stock_quantity": 11}'