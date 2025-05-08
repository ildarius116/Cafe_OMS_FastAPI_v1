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


class OrderItemCreateSchema(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: Optional[int]

    class Config:
        from_attributes = True


class OrderItemUpdateSchema(OrderItemSchema):
    pass


class OrderItemUpdatePartialSchema(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None
