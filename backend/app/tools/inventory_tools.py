from sqlalchemy.orm import Session

from app.database.connection import engine
from app.database.models import Product


def check_inventory(product_id: int) -> dict:
    """
    Check the current inventory for a specific product.

    This is a controlled agent tool.
    The agent receives inventory information without
    getting direct database access.
    """

    with Session(engine) as session:
        product = session.get(Product, product_id)

        if product is None:
            return {
                "success": False,
                "error": "Product not found.",
            }

        return {
            "success": True,
            "product_id": product.id,
            "product_name": product.name,
            "stock_quantity": product.stock_quantity,
            "in_stock": product.stock_quantity > 0,
        }