from typing import List, Optional, Annotated
from annotated_types import Ge, Lt
from pydantic import BaseModel, Field


class MenuItemBaseSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    price: Annotated[float, Ge(0), Lt(1_000_000)]

    class Config:
        from_attributes = True


class MenuItemSchema(MenuItemBaseSchema):
    id: int

    class Config:
        from_attributes = True


class MenuItemsSchema(BaseModel):
    lists: Optional[List[MenuItemSchema]] = None

    class Config:
        from_attributes = True


class MenuItemCreateSchema(MenuItemBaseSchema):
    pass


class MenuItemUpdateSchema(MenuItemBaseSchema):
    pass


class MenuItemUpdatePartialSchema(MenuItemBaseSchema):
    name: Optional[str] = None
    price: Optional[Annotated[float, Ge(0), Lt(1_000_000)]] = None
