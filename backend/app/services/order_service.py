from contextlib import nullcontext
from decimal import Decimal
from threading import Lock

from sqlalchemy.orm import Session

from app.database.connection import USING_LOCAL_FALLBACK
from app.database.models import Customer, Order, OrderItem, Product


_LOCAL_ORDER_LOCK = Lock()


def create_order(
    session: Session,
    customer_name: str,
    customer_email: str,
    product_id: int,
    quantity: int,
) -> Order:
    """Create an order without allowing concurrent inventory oversells.

    PostgreSQL uses SELECT FOR UPDATE. The local SQLite fallback uses a
    process-level lock because SQLite does not provide the same row-locking
    semantics for this in-memory demo database.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    lock = _LOCAL_ORDER_LOCK if USING_LOCAL_FALLBACK else nullcontext()
    with lock:
        try:
            product = (
                session.query(Product)
                .filter(Product.id == product_id)
                .with_for_update()
                .first()
            )

            if product is None:
                raise ValueError("Product not found.")

            if product.stock_quantity < quantity:
                raise ValueError("Insufficient stock.")

            customer = (
                session.query(Customer)
                .filter(Customer.email == customer_email)
                .first()
            )

            if customer is None:
                customer = Customer(
                    name=customer_name,
                    email=customer_email,
                )
                session.add(customer)
                session.flush()

            total_amount = Decimal(product.price) * quantity
            order = Order(
                customer_id=customer.id,
                status="confirmed",
                total_amount=total_amount,
            )
            session.add(order)
            session.flush()

            session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                )
            )
            product.stock_quantity -= quantity
            session.commit()
            session.refresh(order)
            return order
        except Exception:
            session.rollback()
            raise
