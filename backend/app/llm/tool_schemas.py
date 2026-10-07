from typing import Any


def get_tool_schemas() -> list[dict[str, Any]]:
    """
    Return the tool definitions exposed to the LLM.

    These schemas describe what the model is allowed to request.
    The actual execution is still handled by our orchestrator,
    permission layer, and tool registry.
    """

    return [
        {
            "type": "function",
            "name": "search_products",
            "description": (
                "Search the product catalog using an optional text query, "
                "category, and maximum price."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": ["string", "null"],
                        "description": (
                            "Optional product search text, such as "
                            "'lounge chair', 'oak table', or 'floor lamp'."
                        ),
                    },
                    "category": {
                        "type": ["string", "null"],
                        "description": (
                            "Optional product category, such as "
                            "'Seating', 'Tables', 'Lighting', 'Storage', "
                            "or 'Decor'."
                        ),
                    },
                    "max_price": {
                        "type": ["number", "null"],
                        "description": (
                            "Optional maximum product price."
                        ),
                    },
                },
                "required": [
                    "query",
                    "category",
                    "max_price",
                ],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "check_inventory",
            "description": (
                "Check the current inventory quantity and availability "
                "of a specific product."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "The ID of the product to check.",
                    },
                },
                "required": [
                    "product_id",
                ],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "create_order",
            "description": (
                "Prepare an order for a customer. This is a medium-risk "
                "action and requires human approval before execution."
            ),
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "The customer's full name.",
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "The customer's email address.",
                    },
                    "product_id": {
                        "type": "integer",
                        "description": "The ID of the product to order.",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of units to order.",
                    },
                },
                "required": [
                    "customer_name",
                    "customer_email",
                    "product_id",
                    "quantity",
                ],
                "additionalProperties": False,
            },
        },
    ]
