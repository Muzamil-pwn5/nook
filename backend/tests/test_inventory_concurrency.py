from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.database.models import (
    Customer,
    Order,
    OrderItem,
    Product,
)
from app.services.order_service import create_order


TEST_EMAIL_PATTERN = "concurrency_%_test@example.com"


def create_test_product() -> int:
    with Session(engine) as session:
        product = Product(
            name="Concurrency Test Product",
            description=(
                "Temporary product for concurrency testing."
            ),
            price=100.00,
            stock_quantity=1,
            category="Test",
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        return product.id


def get_stock(product_id: int) -> int:
    with Session(engine) as session:
        product = session.get(
            Product,
            product_id,
        )

        assert product is not None

        return product.stock_quantity


def cleanup_test_data(product_id: int) -> None:
    """
    Remove every piece of data created by this test.

    Dependency order:

        OrderItem
            ↓
        Order
            ↓
        Customer
            ↓
        Product
    """

    with Session(engine) as session:

        # Find every test customer.
        test_customers = (
            session.query(Customer)
            .filter(
                Customer.email.like(
                    TEST_EMAIL_PATTERN
                )
            )
            .all()
        )

        customer_ids = [
            customer.id
            for customer in test_customers
        ]

        # Find orders belonging to either:
        #
        # 1. The temporary test product
        # 2. The temporary test customers
        #
        order_ids = set()

        product_order_ids = (
            session.query(OrderItem.order_id)
            .filter(
                OrderItem.product_id == product_id
            )
            .all()
        )

        for row in product_order_ids:
            order_ids.add(row[0])

        if customer_ids:
            customer_order_ids = (
                session.query(Order.id)
                .filter(
                    Order.customer_id.in_(
                        customer_ids
                    )
                )
                .all()
            )

            for row in customer_order_ids:
                order_ids.add(row[0])

        # ------------------------------------------
        # Delete order items first.
        # ------------------------------------------

        if order_ids:
            session.execute(
                delete(OrderItem).where(
                    OrderItem.order_id.in_(
                        list(order_ids)
                    )
                )
            )

        # ------------------------------------------
        # Delete orders second.
        # ------------------------------------------

        if order_ids:
            session.execute(
                delete(Order).where(
                    Order.id.in_(
                        list(order_ids)
                    )
                )
            )

        # ------------------------------------------
        # Delete customers third.
        # ------------------------------------------

        if customer_ids:
            session.execute(
                delete(Customer).where(
                    Customer.id.in_(
                        customer_ids
                    )
                )
            )

        # ------------------------------------------
        # Delete the temporary product last.
        # ------------------------------------------

        session.execute(
            delete(Product).where(
                Product.id == product_id
            )
        )

        session.commit()


def place_order(
    product_id: int,
    customer_number: int,
):
    with Session(engine) as session:
        return create_order(
            session=session,
            customer_name=(
                f"Concurrency Customer "
                f"{customer_number}"
            ),
            customer_email=(
                f"concurrency_{customer_number}_"
                f"test@example.com"
            ),
            product_id=product_id,
            quantity=1,
        )


def test_concurrent_orders_cannot_oversell_inventory():
    """
    Two customers simultaneously attempt to purchase
    one product when only one unit exists.

    Expected:

        One order succeeds.
        One order fails.
        Stock ends at zero.

    The database must never allow stock to become -1.
    """

    product_id = create_test_product()

    barrier = Barrier(2)

    def concurrent_order(
        customer_number: int,
    ):
        barrier.wait()

        try:
            order = place_order(
                product_id=product_id,
                customer_number=customer_number,
            )

            return (
                "success",
                order.id,
            )

        except ValueError as error:
            return (
                "failed",
                str(error),
            )

    try:
        with ThreadPoolExecutor(
            max_workers=2
        ) as executor:

            futures = [
                executor.submit(
                    concurrent_order,
                    1,
                ),
                executor.submit(
                    concurrent_order,
                    2,
                ),
            ]

            results = [
                future.result()
                for future in futures
            ]

        successes = [
            result
            for result in results
            if result[0] == "success"
        ]

        failures = [
            result
            for result in results
            if result[0] == "failed"
        ]

        assert len(successes) == 1
        assert len(failures) == 1

        assert (
            failures[0][1]
            == "Insufficient stock."
        )

        assert get_stock(product_id) == 0

    finally:
        cleanup_test_data(product_id)