from app.llm.agent_loop import LLMAgentLoop


def test_llm_agent_loop_uses_mock_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    agent_loop = LLMAgentLoop()

    result = agent_loop.generate_response(
        "I need a laptop under $650."
    )

    assert result["success"] is True
    assert "Mock LLM response" in result["response"]
    assert "laptop under $650" in result["response"]
