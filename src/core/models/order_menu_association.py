from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixin import IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models import OrderModel, MenuItemModel


class OrderMenuAssociation(Base, IdIntPkMixin):
    __tablename__ = "order_menu_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "menu_item_id",
            name="idx_unique_order_menu",
        ),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    price: Mapped[float] = mapped_column(Numeric(8, 2), default=0, server_default="0")
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")

    order: Mapped["OrderModel"] = relationship(
        back_populates="menu_items_details",
    )
    menu_item: Mapped["MenuItemModel"] = relationship(back_populates="orders_details")

    def __repr__(self):
        return (
            f"OrderMenuAssociation("
            f"order_id={self.order_id}, "
            f"menu_item_id={self.menu_item_id}, "
            f"menu_item={self.menu_item}, "
            f"price={self.price}, "
            f"quantity={self.quantity}"
            f")"
        )
