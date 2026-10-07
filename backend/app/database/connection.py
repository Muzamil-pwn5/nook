import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session

from app.database.catalog import storefront_products
from app.database.models import Base, Product


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("mysql+mysqldb://"):
    DATABASE_URL = DATABASE_URL.replace("mysql+mysqldb://", "mysql+pymysql://", 1)
elif DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
USING_LOCAL_FALLBACK = not bool(DATABASE_URL)

if USING_LOCAL_FALLBACK:
    # A shared in-memory database keeps the demo and test flows functional
    # without requiring credentials or a running PostgreSQL instance.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
    if DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, **engine_kwargs)


def _seed_local_products() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.scalars(select(Product)).first() is not None:
            return
        session.add_all(storefront_products())
        session.commit()


if USING_LOCAL_FALLBACK:
    _seed_local_products()


def test_database_connection() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
