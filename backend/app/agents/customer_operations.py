from app.agents.orchestrator import AgentOrchestrator


class CustomerOperationsAgent:
    """
    Customer-facing agent responsible for routine e-commerce operations.

    The agent does not access the database directly.
    It can only act through the orchestrator and registered tools.
    """

    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    def search_products(
        self,
        query: str | None = None,
        category: str | None = None,
        max_price: float | None = None,
    ) -> dict:
        return self.orchestrator.execute_tool(
            tool_name="search_products",
            arguments={
                "query": query,
                "category": category,
                "max_price": max_price,
            },
        )

    def check_inventory(self, product_id: int) -> dict:
        return self.orchestrator.execute_tool(
            tool_name="check_inventory",
            arguments={
                "product_id": product_id,
            },
        )

    def create_order(
        self,
        customer_name: str,
        customer_email: str,
        product_id: int,
        quantity: int,
        approved: bool = False,
    ) -> dict:
        return self.orchestrator.execute_tool(
            tool_name="create_order",
            arguments={
                "customer_name": customer_name,
                "customer_email": customer_email,
                "product_id": product_id,
                "quantity": quantity,
            },
            approved=approved,
        )