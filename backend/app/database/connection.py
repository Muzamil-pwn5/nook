import json
import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database.catalog import storefront_products
from app.database.models import Base, Product

load_dotenv()


def _normalise_database_url(raw_url: str | None) -> tuple[str | None, dict[str, object]]:
    if not raw_url:
        return None, {}
    url = raw_url
    if url.startswith("mysql+mysqldb://"):
        url = url.replace("mysql+mysqldb://", "mysql+pymysql://", 1)
    elif url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)

    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True)
    connect_args: dict[str, object] = {}
    clean_query: list[tuple[str, str]] = []
    for key, value in query:
        if key.lower() != "ssl":
            clean_query.append((key, value))
            continue
        try:
            ssl_options = json.loads(value)
        except json.JSONDecodeError:
            ssl_options = {}
        if isinstance(ssl_options, dict):
            connect_args["ssl"] = {
                "check_hostname": bool(ssl_options.get("rejectUnauthorized", True)),
            }

    clean_url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(clean_query), parts.fragment))
    return clean_url, connect_args


DATABASE_URL, DATABASE_CONNECT_ARGS = _normalise_database_url(os.getenv("DATABASE_URL"))
USING_LOCAL_FALLBACK = not bool(DATABASE_URL) or DATABASE_URL.startswith("sqlite")

if not DATABASE_URL:
    DATABASE_URL = "sqlite://"

engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    if DATABASE_URL == "sqlite://":
        engine_kwargs["poolclass"] = StaticPool
elif DATABASE_CONNECT_ARGS:
    engine_kwargs["connect_args"] = DATABASE_CONNECT_ARGS

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
