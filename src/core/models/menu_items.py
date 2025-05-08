from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from src.core.models import Base

# from src.api_v1.menu_items.schemas import MenuItemSchema

if TYPE_CHECKING:
    from src.core.models import OrderItemModel


class MenuItemModel(Base):
    __tablename__ = "menu_items"

    name: Mapped[str] = mapped_column(String(42))
    # price: Mapped[Optional[float]] = mapped_column(Numeric(8, 1), name="Цена")
    price: Mapped[Optional[float]] = mapped_column(Numeric(8, 1))

    order_items: Mapped[List["OrderItemModel"]] = relationship(
        back_populates="menu_item"
    )

    # def to_read_model(self):
    #     return MenuItemSchema(
    #         id=self.id,
    #         name=self.name,
    #         price=self.price,
    #     )

    def __str__(self) -> str:
        return (
            f"<Menu_item(id={self.id}, " f"name={self.name}, " f"price={self.price})>"
        )

    def __repr__(self) -> str:
        return str(self)

    class Meta:
        name: str = "Блюдо"
        name_plural: str = "Блюда"
