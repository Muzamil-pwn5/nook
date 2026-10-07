from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.database.models import Product


def search_products(
    query: str | None = None,
    category: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search products using controlled business criteria.

    This function is an agent tool.
    The agent can request product information through this
    function without getting direct database access.
    """

    with Session(engine) as session:
        statement = select(Product)

        if query:
            search_term = f"%{query.lower()}%"
            statement = statement.where(
                Product.name.ilike(search_term)
                | Product.description.ilike(search_term)
            )

        if category:
            statement = statement.where(
                Product.category.ilike(category)
            )

        if max_price is not None:
            statement = statement.where(
                Product.price <= max_price
            )

        statement = statement.order_by(Product.id)

        products = session.scalars(statement).all()

        return [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock_quantity": product.stock_quantity,
                "category": product.category,
            }
            for product in products
        ]