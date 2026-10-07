from app.agents.conversation_state import ConversationState
from app.agents.customer_info import extract_customer_info
from app.agents.customer_operations import CustomerOperationsAgent
from app.agents.decision_engine import CustomerDecisionEngine


class CustomerAgentRunner:
    def __init__(self):
        self.decision_engine = CustomerDecisionEngine()
        self.customer_agent = CustomerOperationsAgent()
        self.state = ConversationState()

    def handle_message(self, user_message: str) -> dict:
        # If we are waiting for customer information for a pending order,
        # process the new message as customer information first.
        if self.state.pending_action == "create_order":
            customer_info = extract_customer_info(user_message)

            if customer_info["name"]:
                self.state.customer_name = customer_info["name"]

            if customer_info["email"]:
                self.state.customer_email = customer_info["email"]

            if (
                self.state.customer_name
                and self.state.customer_email
            ):
                product_id = self.state.pending_arguments["product_id"]
                quantity = self.state.pending_arguments["quantity"]

                result = self.customer_agent.create_order(
                    customer_name=self.state.customer_name,
                    customer_email=self.state.customer_email,
                    product_id=product_id,
                    quantity=quantity,
                    approved=False,
                )

                return {
                    "success": result["success"],
                    "type": "tool_result",
                    "intent": "create_order",
                    "tool": "create_order",
                    "result": result,
                }

            return {
                "success": False,
                "type": "customer_information_required",
                "message": (
                    "I still need both your name and email "
                    "before I can prepare the order."
                ),
            }

        decision = self.decision_engine.decide(
            user_message,
            self.state,
        )

        if decision.requires_clarification:
            return {
                "success": False,
                "type": "clarification",
                "message": decision.clarification_message,
                "decision": decision,
            }

        if decision.tool_name == "search_products":
            result = self.customer_agent.search_products(
                query=decision.arguments.get("query"),
                category=decision.arguments.get("category"),
                max_price=decision.arguments.get("max_price"),
            )

            if result["success"]:
                products = result["result"]
                self.state.remember_products(products)

            return {
                "success": result["success"],
                "type": "tool_result",
                "intent": decision.intent,
                "tool": decision.tool_name,
                "result": result,
                "state": {
                    "selected_product_id": self.state.selected_product_id,
                    "search_result_count": len(
                        self.state.last_search_results
                    ),
                },
            }

        if decision.tool_name == "create_order":
            product_id = decision.arguments.get("product_id")
            quantity = decision.arguments.get("quantity", 1)

            if product_id is None:
                return {
                    "success": False,
                    "type": "clarification",
                    "message": "Which product would you like to buy?",
                }

            if (
                self.state.customer_name is None
                or self.state.customer_email is None
            ):
                self.state.pending_action = "create_order"
                self.state.pending_arguments = {
                    "product_id": product_id,
                    "quantity": quantity,
                }

                return {
                    "success": False,
                    "type": "customer_information_required",
                    "message": (
                        "I can place the order, but I need "
                        "your name and email first."
                    ),
                    "pending_action": self.state.pending_action,
                    "pending_arguments": self.state.pending_arguments,
                }

            result = self.customer_agent.create_order(
                customer_name=self.state.customer_name,
                customer_email=self.state.customer_email,
                product_id=product_id,
                quantity=quantity,
                approved=False,
            )

            return {
                "success": result["success"],
                "type": "tool_result",
                "intent": decision.intent,
                "tool": decision.tool_name,
                "result": result,
            }

        return {
            "success": False,
            "type": "unsupported",
            "message": (
                f"The operation '{decision.intent}' "
                "is not implemented yet."
            ),
        }