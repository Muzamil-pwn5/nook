from app.llm.agent_runner import LLMAgentRunner


class LLMAgentLoop:
    """
    Backward-compatible entry point for running the LLM agent.

    The actual multi-step reasoning and tool execution now lives
    inside LLMAgentRunner.
    """

    def __init__(self):
        self.runner = LLMAgentRunner()

    def generate_response(
        self,
        user_message: str,
    ) -> dict:
        """
        Run the complete agent workflow for one user message.
        """

        return self.runner.run(
            user_message=user_message,
        )