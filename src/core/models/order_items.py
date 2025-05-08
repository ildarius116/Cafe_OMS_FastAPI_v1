from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from src.core.models import Base

# from src.api_v1.orders.schemas import OrderItemSchema

if TYPE_CHECKING:
    from src.core.models import OrderModel, MenuItemModel


class OrderItemModel(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    # price: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), name="Цена")
    price: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    quantity: Mapped[int] = mapped_column(default=1)

    # Связи
    order: Mapped["OrderModel"] = relationship(back_populates="order_items")
    menu_item: Mapped["MenuItemModel"] = relationship(back_populates="order_items")

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
        self.order.save()

    # def to_read_model(self):
    #     return OrderItemSchema(
    #         id=self.id,
    #         order_id=self.order_id,
    #         menu_item_id=self.menu_item_id,
    #         price=self.price,
    #         quantity=self.quantity,
    #         # menu_item=self.menu_item.to_read_model() if self.menu_item else None,
    #     )

    def __repr__(self) -> str:
        return (
            f"<Order_item(id={self.id}, "
            f"order_id={self.order_id}, "
            f"menu_item_id={self.menu_item_id}, "
            f"price={self.price})>"
        )
