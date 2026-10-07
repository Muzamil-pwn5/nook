from pydantic import BaseModel, EmailStr, Field


class CreateOrderRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    customer_email: EmailStr
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CreateOrderResponse(BaseModel):
    order_id: int
    customer_id: int
    status: str
    total_amount: float