from app.agents.orchestrator import AgentOrchestrator
from app.llm.tool_call import ToolCall


class LLMToolExecutor:
    """
    Executes tool calls requested by an LLM.

    The LLM never gets direct access to business tools or the database.
    Every requested action goes through the existing orchestrator,
    permission policies, and audit logging.
    """

    def __init__(
        self,
        orchestrator: AgentOrchestrator | None = None,
    ):
        self.orchestrator = orchestrator or AgentOrchestrator()

    def execute(
        self,
        tool_call: ToolCall,
        approved: bool = False,
    ) -> dict:
        """
        Execute one LLM-requested tool call through the orchestrator.
        """

        return self.orchestrator.execute_tool(
            tool_name=tool_call.tool_name,
            arguments=tool_call.arguments,
            approved=approved,
        )