from app.tools.inventory_tools import check_inventory
from app.tools.order_tools import create_order_tool
from app.tools.product_tools import search_products


TOOL_REGISTRY = {
    "search_products": {
        "function": search_products,
        "description": (
            "Search the product catalog using a text query, category, "
            "and/or maximum price."
        ),
    },
    "check_inventory": {
        "function": check_inventory,
        "description": (
            "Check the current stock quantity and availability "
            "of a specific product."
        ),
    },
    "create_order": {
        "function": create_order_tool,
        "description": (
            "Create a confirmed customer order for a product and "
            "quantity after required customer information is provided."
        ),
    },
}