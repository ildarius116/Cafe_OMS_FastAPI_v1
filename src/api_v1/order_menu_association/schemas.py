from pydantic import BaseModel


class OrderMenuAssociationBaseSchema(BaseModel):
    order_id: int
    menu_item_id: int
    price: float
    quantity: int

    class Config:
        from_attributes = True


class OrderMenuAssociationSchema(OrderMenuAssociationBaseSchema):
    id: int
