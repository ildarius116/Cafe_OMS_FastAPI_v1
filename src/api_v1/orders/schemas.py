from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.api_v1.order_menu_association.schemas import OrderMenuAssociationSchema


class OrderBaseSchema(BaseModel):
    table_number: int = Field(ge=1, le=100, description="Номер стола")
    menu_items_details: Optional[List["OrderMenuAssociationSchema"]] = None
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
    menu_items_details: Optional[List["OrderMenuAssociationSchema"]] = None
    total_price: Optional[float] = None
    # updated_at: Optional[datetime] = None


class OrdersSchema(BaseModel):
    lists: Optional[List[OrderSchema]] = None
