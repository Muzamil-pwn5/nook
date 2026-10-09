from fastapi import FastAPI
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.agent import router as agent_router
from app.api.auth import router as auth_router
from app.api.orders import router as orders_router
from app.database.connection import engine
from app.database.models import Product


STATIC_DIR = Path(__file__).resolve().parents[2] / "frontend" / "static-dist"
INDEX_FILE = STATIC_DIR / "index.html"

app = FastAPI(
    title="FYP Agentic AI Platform",
    version="1.0.0",
)

app.include_router(orders_router)
app.include_router(agent_router)
app.include_router(auth_router)

if (STATIC_DIR / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/", include_in_schema=False)
def root():
    if INDEX_FILE.is_file():
        return FileResponse(INDEX_FILE, media_type="text/html")
    return {
        "status": "online",
        "service": "FYP Agentic AI Platform",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    with Session(engine) as session:
        products = session.scalars(select(Product)).all()

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


@app.get("/{path:path}", include_in_schema=False)
def serve_frontend(path: str):
    if not INDEX_FILE.is_file():
        raise HTTPException(status_code=404, detail="Frontend bundle is not available.")

    candidate = (STATIC_DIR / path).resolve()
    try:
        candidate.relative_to(STATIC_DIR.resolve())
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Not found.") from error

    if path and candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(INDEX_FILE, media_type="text/html")
