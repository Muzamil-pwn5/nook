from dataclasses import dataclass, field


@dataclass
class ConversationState:
    customer_name: str | None = None
    customer_email: str | None = None

    last_search_results: list[dict] = field(default_factory=list)
    selected_product_id: int | None = None

    pending_action: str | None = None
    pending_arguments: dict = field(default_factory=dict)

    def remember_products(self, products: list[dict]) -> None:
        self.last_search_results = products

        if len(products) == 1:
            self.selected_product_id = products[0]["id"]

    def select_product(self, product_id: int) -> bool:
        for product in self.last_search_results:
            if product["id"] == product_id:
                self.selected_product_id = product_id
                return True

        return False

    def get_selected_product(self) -> dict | None:
        if self.selected_product_id is None:
            return None

        for product in self.last_search_results:
            if product["id"] == self.selected_product_id:
                return product

        return None

    def clear_pending_action(self) -> None:
        self.pending_action = None
        self.pending_arguments.clear()