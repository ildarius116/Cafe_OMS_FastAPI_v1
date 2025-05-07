from typing import List, Optional, Annotated
from annotated_types import Ge, Lt
from pydantic import BaseModel, Field


class MenuItemSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    price: Annotated[float, Ge(0), Lt(1_000_000)]

    class Config:
        from_attributes = True


class MenuItemsSchema(BaseModel):
    lists: Optional[List[MenuItemSchema]] = None
