from app.llm.response import LLMResponse
from app.llm.tool_call import ToolCall
from app.llm.tool_executor import LLMToolExecutor


class LLMToolLoop:
    """
    Processes tool calls returned by an LLM.

    The LLM proposes actions.
    The tool executor sends those actions through the orchestrator,
    permission policies, and audit logging.

    This component does not give the LLM direct database access.
    """

    def __init__(
        self,
        tool_executor: LLMToolExecutor | None = None,
    ):
        self.tool_executor = tool_executor or LLMToolExecutor()

    def execute_response(
        self,
        response: LLMResponse,
        approved: bool = False,
    ) -> list[dict]:
        """
        Execute every tool call contained in an LLM response.

        Returns one result for each requested tool call.
        """

        results = []

        for raw_tool_call in response.tool_calls:
            tool_call = ToolCall(
                call_id=raw_tool_call["call_id"],
                tool_name=raw_tool_call["tool_name"],
                arguments=raw_tool_call["arguments"],
            )

            result = self.tool_executor.execute(
                tool_call=tool_call,
                approved=approved,
            )

            results.append(
                {
                    "call_id": tool_call.call_id,
                    "tool_name": tool_call.tool_name,
                    "result": result,
                }
            )

        return results