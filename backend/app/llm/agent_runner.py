import json
from typing import Any

from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.provider_factory import get_llm_provider
from app.llm.system_prompt import CUSTOMER_OPERATIONS_SYSTEM_PROMPT
from app.llm.tool_loop import LLMToolLoop


class LLMAgentRunner:
    """
    Runs a multi-step LLM agent workflow.

    The runner supports:
    - Normal tool execution
    - Permission checks
    - Human approval pauses
    - Resuming an interrupted workflow
    - Iteration limits
    - Provider injection for testing
    """

    def __init__(
        self,
        provider: LLMProvider | None = None,
        tool_loop: LLMToolLoop | None = None,
        max_iterations: int = 5,
    ):
        if max_iterations <= 0:
            raise ValueError(
                "max_iterations must be greater than zero."
            )

        self.provider = provider or get_llm_provider()
        self.tool_loop = tool_loop or LLMToolLoop()
        self.max_iterations = max_iterations

    def run(
        self,
        user_message: str,
        conversation: AgentConversation | None = None,
    ) -> dict:
        """
        Start or continue an agent workflow.
        """

        conversation = conversation or AgentConversation()

        conversation.add_user_message(
            user_message
        )

        return self._continue(
            conversation=conversation,
            approved=False,
        )

    def resume_after_approval(
        self,
        conversation: AgentConversation,
        tool_call_id: str,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict:
        """
        Resume a paused workflow after human approval.

        The approved action is executed through the same
        ToolLoop -> ToolExecutor -> Orchestrator -> Permission
        architecture used during normal execution.
        """

        result = self.tool_loop.tool_executor.orchestrator.execute_tool(
            tool_name=tool_name,
            arguments=arguments,
            approved=True,
        )

        conversation.add_tool_result(
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            content=json.dumps(
                result,
                default=str,
            ),
        )

        if not result.get("success"):
            return {
                "success": False,
                "type": "tool_execution_failed",
                "response": result.get(
                    "error",
                    "The approved action could not be completed.",
                ),
                "conversation": conversation,
            }

        return self._continue(
            conversation=conversation,
            approved=False,
        )

    def _continue(
        self,
        conversation: AgentConversation,
        approved: bool = False,
    ) -> dict:
        """
        Continue an existing agent conversation.
        """

        for iteration in range(self.max_iterations):
            response = self.provider.generate(
                system_prompt=CUSTOMER_OPERATIONS_SYSTEM_PROMPT,
                conversation=conversation,
            )

            if not response.tool_calls:
                if response.text:
                    conversation.add_assistant_message(
                        response.text
                    )

                return {
                    "success": True,
                    "type": "final_response",
                    "response": response.text,
                    "iterations": iteration + 1,
                    "conversation": conversation,
                }

            for tool_call in response.tool_calls:
                conversation.add_assistant_tool_call(
                    tool_call_id=tool_call["call_id"],
                    tool_name=tool_call["tool_name"],
                    arguments=tool_call["arguments"],
                )

            tool_results = self.tool_loop.execute_response(
                response,
                approved=approved,
            )

            for tool_result in tool_results:
                result = tool_result["result"]

                if (
                    isinstance(result, dict)
                    and result.get("requires_approval")
                ):
                    return {
                        "success": False,
                        "type": "approval_required",
                        "response": (
                            "This action requires human approval "
                            "before it can be executed."
                        ),
                        "pending_action": {
                            "call_id": tool_result["call_id"],
                            "tool_name": tool_result["tool_name"],
                            "arguments": next(
                                (
                                    call["arguments"]
                                    for call in response.tool_calls
                                    if call["call_id"]
                                    == tool_result["call_id"]
                                ),
                                {},
                            ),
                            "risk": result.get("risk"),
                        },
                        "conversation": conversation,
                    }

                conversation.add_tool_result(
                    tool_call_id=tool_result["call_id"],
                    tool_name=tool_result["tool_name"],
                    content=json.dumps(
                        result,
                        default=str,
                    ),
                )

        return {
            "success": False,
            "type": "iteration_limit",
            "response": (
                "I could not complete the request within "
                "the allowed number of reasoning steps."
            ),
            "iterations": self.max_iterations,
            "conversation": conversation,
        }
