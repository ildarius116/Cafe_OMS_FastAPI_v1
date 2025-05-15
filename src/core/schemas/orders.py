from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from src.core.schemas.order_menu_association import OrderMenuAssociationSchema


class OrderBaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    table_number: int = Field(ge=1, le=100, description="Номер стола")
    menu_items_details: Optional[List["OrderMenuAssociationSchema"]] = None
    total_price: Optional[float] = Field(0, ge=0, description="Общая стоимость")
    status: str = Field(default="pending")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrderSchema(OrderBaseSchema):
    id: int


class OrderCreateSchema(BaseModel):
    table_number: int = Field(ge=1, le=100, description="Номер стола")
    status: str = Field(default="pending")


class OrderUpdateSchema(BaseModel):
    table_number: int
    status: str
    menu_items_details: List["OrderMenuAssociationSchema"]
    total_price: float


class OrderFilterSchema(BaseModel):
    table_number: Optional[int] = None
    status: Optional[str] = None


class OrderUpdatePartialSchema(BaseModel):
    table_number: Optional[int] = None
    status: Optional[str] = None
    menu_items_details: Optional[List["OrderMenuAssociationSchema"]] = None
    total_price: Optional[float] = None


class OrdersSchema(BaseModel):
    lists: Optional[List[OrderSchema]] = None
