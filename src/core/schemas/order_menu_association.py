from pydantic import BaseModel, ConfigDict


class OrderMenuAssociationBaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    order_id: int
    menu_item_id: int
    price: float
    quantity: int


class OrderMenuAssociationSchema(OrderMenuAssociationBaseSchema):
    id: int


class OrderMenuAssociationAddSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    menu_item_id: int
    quantity: int
