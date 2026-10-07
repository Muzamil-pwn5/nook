from app.database.connection import engine
from app.services.order_service import create_order
from sqlalchemy.orm import Session


def create_order_tool(
    customer_name: str,
    customer_email: str,
    product_id: int,
    quantity: int,
) -> dict:
    """
    Controlled tool for creating an order.

    The agent can request an order through this function,
    but the actual database operation remains inside the
    business service layer.
    """

    if not customer_name.strip():
        return {
            "success": False,
            "error": "Customer name is required.",
        }

    if not customer_email.strip():
        return {
            "success": False,
            "error": "Customer email is required.",
        }

    if product_id <= 0:
        return {
            "success": False,
            "error": "Product ID must be greater than zero.",
        }

    if quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than zero.",
        }

    try:
        with Session(engine) as session:
            order = create_order(
                session=session,
                customer_name=customer_name,
                customer_email=customer_email,
                product_id=product_id,
                quantity=quantity,
            )

            return {
                "success": True,
                "order_id": order.id,
                "customer_id": order.customer_id,
                "status": order.status,
                "total_amount": float(order.total_amount),
            }

    except ValueError as error:
        return {
            "success": False,
            "error": str(error),
        }