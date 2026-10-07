from sqlalchemy import select

from app.database.catalog import storefront_products
from app.database.connection import engine
from app.database.models import Base, Product
from sqlalchemy.orm import Session


def seed_products() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        existing_products = session.scalars(select(Product)).all()

        if existing_products:
            print("Products already exist. Nothing to seed.")
            return

        products = storefront_products()

        session.add_all(products)
        session.commit()

        print(f"Seeded {len(products)} products successfully.")


if __name__ == "__main__":
    seed_products()
