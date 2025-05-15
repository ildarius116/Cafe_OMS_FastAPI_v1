from typing import List, Optional, Annotated
from annotated_types import Ge, Lt
from pydantic import BaseModel, Field, ConfigDict


class MenuItemBaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=3, max_length=20)
    price: Annotated[float, Ge(0), Lt(1_000_000)]


class MenuItemSchema(MenuItemBaseSchema):
    id: int


class MenuItemCreateSchema(MenuItemBaseSchema):
    pass


class MenuItemUpdateSchema(MenuItemBaseSchema):
    pass


class MenuItemUpdatePartialSchema(MenuItemBaseSchema):
    name: Optional[str] = None
    price: Optional[Annotated[float, Ge(0), Lt(1_000_000)]] = None
