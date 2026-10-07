from dataclasses import dataclass
import re

from app.agents.conversation_state import ConversationState


@dataclass
class AgentDecision:
    intent: str
    tool_name: str | None
    arguments: dict
    requires_clarification: bool
    clarification_message: str | None = None


class CustomerDecisionEngine:
    """
    Temporary deterministic decision engine.

    This is a bridge until a real LLM is connected.
    It interprets common customer requests and uses conversation
    state when the user refers to previously selected products.
    """

    def decide(
        self,
        user_message: str,
        state: ConversationState | None = None,
    ) -> AgentDecision:
        message = user_message.strip()

        if not message:
            return AgentDecision(
                intent="unknown",
                tool_name=None,
                arguments={},
                requires_clarification=True,
                clarification_message=(
                    "What would you like me to help you with?"
                ),
            )

        lower_message = message.lower()

        if self._is_purchase_request(lower_message):
            return self._decide_purchase(message, state)

        if any(
            keyword in lower_message
            for keyword in [
                "find",
                "search",
                "looking for",
                "show me",
                "need",
            ]
        ):
            return self._decide_product_search(message)

        return AgentDecision(
            intent="unknown",
            tool_name=None,
            arguments={},
            requires_clarification=True,
            clarification_message=(
                "I understand the request, but I don't yet know "
                "which customer operation you want me to perform."
            ),
        )

    def _decide_purchase(
        self,
        message: str,
        state: ConversationState | None,
    ) -> AgentDecision:
        product_id = self._extract_product_id(message)
        quantity = self._extract_quantity(message)

        if product_id is None and state is not None:
            if self._refers_to_previous_product(message):
                product_id = state.selected_product_id

        if product_id is None:
            return AgentDecision(
                intent="create_order",
                tool_name="create_order",
                arguments={},
                requires_clarification=True,
                clarification_message=(
                    "Which product would you like to buy?"
                ),
            )

        return AgentDecision(
            intent="create_order",
            tool_name="create_order",
            arguments={
                "product_id": product_id,
                "quantity": quantity,
            },
            requires_clarification=False,
        )

    def _decide_product_search(
        self,
        message: str,
    ) -> AgentDecision:
        max_price = self._extract_price(message)

        category = None
        lower_message = message.lower()

        if "laptop" in lower_message:
            category = "Laptops"
        elif "keyboard" in lower_message:
            category = "Accessories"
        elif "mouse" in lower_message:
            category = "Accessories"
        elif "headphone" in lower_message:
            category = "Audio"

        query = None

        if category == "Laptops":
            query = "laptop"
        elif category == "Audio":
            query = "headphones"
        elif "mouse" in lower_message:
            query = "mouse"
        elif "keyboard" in lower_message:
            query = "keyboard"

        return AgentDecision(
            intent="search_products",
            tool_name="search_products",
            arguments={
                "query": query,
                "category": category,
                "max_price": max_price,
            },
            requires_clarification=False,
        )

    @staticmethod
    def _is_purchase_request(message: str) -> bool:
        return any(
            keyword in message
            for keyword in [
                "buy",
                "order",
                "purchase",
                "get that",
                "get this",
                "take that",
                "take this",
            ]
        )

    @staticmethod
    def _refers_to_previous_product(message: str) -> bool:
        references = [
            "that one",
            "this one",
            "that",
            "this",
            "the one",
            "the product",
            "the laptop",
        ]

        return any(reference in message for reference in references)

    @staticmethod
    def _extract_product_id(message: str) -> int | None:
        patterns = [
            r"product\s*(?:id)?\s*[:#]?\s*(\d+)",
            r"\bitem\s*(?:id)?\s*[:#]?\s*(\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())

            if match:
                return int(match.group(1))

        return None

    @staticmethod
    def _extract_quantity(message: str) -> int:
        patterns = [
            r"\b(\d+)\s*(?:x|units?|items?|pieces?)\b",
            r"\bquantity\s*[:=]?\s*(\d+)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())

            if match:
                quantity = int(match.group(1))

                if quantity > 0:
                    return quantity

        return 1

    @staticmethod
    def _extract_price(message: str) -> float | None:
        patterns = [
            r"(?:under|below|less than|up to|max(?:imum)?(?: price)?(?: of)?)\s*\$?\s*(\d+(?:\.\d+)?)",
            r"\$\s*(\d+(?:\.\d+)?)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())

            if match:
                return float(match.group(1))

        return None