from typing import List, Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field


class OrderItemSchema(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: Optional[int]
    price: Optional[float]

    class Config:
        from_attributes = True


class OrderBaseSchema(BaseModel):
    table_number: int = Field(ge=1, le=100, description="Номер стола")
    order_items: Optional[List[OrderItemSchema]] = None
    total_price: Optional[float] = Field(0, ge=0, description="Общая стоимость")
    status: str = Field(default="pending")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderSchema(OrderBaseSchema):
    id: int


class OrderCreateSchema(BaseModel):
    table_number: int = Field(ge=1, le=100, description="Номер стола")


class OrderUpdateSchema(OrderBaseSchema):
    pass


class OrderUpdatePartialSchema(BaseModel):
    table_number: Optional[int] = None
    status: Optional[str] = None
    order_items: Optional[List[OrderItemSchema]] = None
    total_price: Optional[float] = None
    # updated_at: Optional[datetime] = None


class OrdersSchema(BaseModel):
    lists: Optional[List[OrderSchema]] = None
