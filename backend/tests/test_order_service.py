from sqlalchemy.orm import Session

from app.database.connection import engine
from app.database.models import Order, OrderItem, Customer, Product
from app.services.order_service import create_order


def main() -> None:
    test_email = "test.customer@example.com"

    with Session(engine) as session:
        product = session.get(Product, 1)

        if product is None:
            raise RuntimeError("Product with ID 1 was not found.")

        original_stock = product.stock_quantity

        order = create_order(
            session=session,
            customer_name="Test Customer",
            customer_email=test_email,
            product_id=product.id,
            quantity=1,
        )

        print("Order created successfully.")
        print(f"Order ID: {order.id}")
        print(f"Customer ID: {order.customer_id}")
        print(f"Total: {order.total_amount}")
        print(f"Product stock before: {original_stock}")
        print(f"Product stock after: {product.stock_quantity}")

        if product.stock_quantity != original_stock - 1:
            raise RuntimeError("Inventory was not reduced correctly.")

        if order.status != "confirmed":
            raise RuntimeError("Order was not confirmed correctly.")

        # Clean up the test data
        session.delete(order)
        session.flush()

        customer = (
            session.query(Customer)
            .filter(Customer.email == test_email)
            .first()
        )

        if customer is not None:
            session.delete(customer)

        product.stock_quantity = original_stock

        session.commit()

        print("Test data cleaned up.")
        print("Order service test passed.")


if __name__ == "__main__":
    main()