from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.schemas.order import CreateOrderRequest, CreateOrderResponse
from app.services.order_service import create_order


router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=CreateOrderResponse)
def create_order_endpoint(
    request: CreateOrderRequest,
    db: Session = Depends(get_db),
):
    try:
        order = create_order(
            session=db,
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            product_id=request.product_id,
            quantity=request.quantity,
        )

        return CreateOrderResponse(
            order_id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            total_amount=float(order.total_amount),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )