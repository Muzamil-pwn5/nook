from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.agents.customer_agent_runner import CustomerAgentRunner


class ApprovalService:
    """
    Handles explicit human approval for pending agent actions.

    The service does not create orders directly.
    It asks the Customer Operations Agent to execute the
    already-pending action with explicit approval.
    """

    def approve_pending_order(
        self,
        agent_runner: "CustomerAgentRunner",
    ) -> dict:
        state = agent_runner.state

        if state.pending_action != "create_order":
            return {
                "success": False,
                "error": "There is no pending order awaiting approval.",
            }

        if (
            state.customer_name is None
            or state.customer_email is None
        ):
            return {
                "success": False,
                "error": (
                    "Customer information is incomplete. "
                    "Name and email are required."
                ),
            }

        product_id = state.pending_arguments.get("product_id")
        quantity = state.pending_arguments.get("quantity", 1)

        if product_id is None:
            return {
                "success": False,
                "error": "Pending order has no product.",
            }

        result = agent_runner.customer_agent.create_order(
            customer_name=state.customer_name,
            customer_email=state.customer_email,
            product_id=product_id,
            quantity=quantity,
            approved=True,
        )

        if result["success"]:
            state.clear_pending_action()

        return result