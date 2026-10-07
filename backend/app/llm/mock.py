from app.llm.base import LLMProvider
from app.llm.conversation import AgentConversation
from app.llm.response import LLMResponse


class MockLLMProvider(LLMProvider):
    """
    Deterministic local LLM simulator.

    Search flow:

        user
        -> search_products
        -> check_inventory
        -> final response

    Purchase flow:

        user
        -> search_products
        -> create_order
        -> approval_required
        -> final response

    The mock is stateless between requests.
    The conversation itself determines the next action.
    """

    def generate(
        self,
        system_prompt: str,
        conversation: AgentConversation,
    ) -> LLMResponse:

        user_message = self._get_user_message(
            conversation
        )

        is_purchase = any(
            word in user_message
            for word in (
                "buy",
                "purchase",
                "order",
            )
        )

        if is_purchase:
            return self._purchase_flow(
                conversation
            )

        return self._search_flow(
            conversation
        )

    def _get_user_message(
        self,
        conversation: AgentConversation,
    ) -> str:

        for message in conversation.messages:
            if message.role == "user":
                return message.content.lower()

        return ""

    def _get_completed_tools(
        self,
        conversation: AgentConversation,
    ) -> list[str]:

        completed_tools = []

        for message in conversation.messages:
            if (
                message.role == "tool"
                and message.tool_name
            ):
                completed_tools.append(
                    message.tool_name
                )

        return completed_tools

    def _purchase_flow(
        self,
        conversation: AgentConversation,
    ) -> LLMResponse:

        completed_tools = self._get_completed_tools(
            conversation
        )

        # Step 1: Search for the requested product.
        if "search_products" not in completed_tools:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "mock_search_purchase_1",
                        "tool_name": "search_products",
                        "arguments": {
                            "query": "HP Pavilion 14",
                            "category": None,
                            "max_price": None,
                        },
                    }
                ]
            )

        # Step 2: Request order creation.
        #
        # The orchestrator will stop this action and
        # require human approval before execution.
        if "create_order" not in completed_tools:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "mock_order_1",
                        "tool_name": "create_order",
                        "arguments": {
                            "customer_name": "Ahmed Khan",
                            "customer_email": (
                                "ahmed.test@example.com"
                            ),
                            "product_id": 2,
                            "quantity": 1,
                        },
                    }
                ]
            )

        # Step 3: Final response after approval.
        return LLMResponse(
            text=(
                "Your order has been successfully "
                "created after approval."
            )
        )

    def _search_flow(
        self,
        conversation: AgentConversation,
    ) -> LLMResponse:

        completed_tools = self._get_completed_tools(
            conversation
        )

        # Step 1: Search for products.
        if "search_products" not in completed_tools:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "mock_search_1",
                        "tool_name": "search_products",
                        "arguments": {
                            "query": "laptop",
                            "category": None,
                            "max_price": 650,
                        },
                    }
                ]
            )

        # Step 2: Check inventory.
        if "check_inventory" not in completed_tools:
            return LLMResponse(
                tool_calls=[
                    {
                        "call_id": "mock_inventory_1",
                        "tool_name": "check_inventory",
                        "arguments": {
                            "product_id": 2,
                        },
                    }
                ]
            )

        # Step 3: Final response.
        #
        # Keep the original wording because the existing
        # automated test verifies this response.
        return LLMResponse(
            text=(
                "Mock LLM response. I received the "
                "request for a laptop under $650. "
                "I found the HP Pavilion 14 for "
                "$649.99 and confirmed that it is "
                "currently in stock."
            )
        )