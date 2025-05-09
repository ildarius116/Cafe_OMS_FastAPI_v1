from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.core.models import Base

# from src.api_v1.orders.schemas import OrderMenuAssociationSchema

if TYPE_CHECKING:
    from src.core.models import OrderModel, MenuItemModel

    # from src.api_v1.menu_items.schemas import MenuItemSchema


class OrderMenuAssociation(Base):
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

    order: Mapped["OrderModel"] = relationship(back_populates="menu_items_details")
    menu_item: Mapped["MenuItemModel"] = relationship(back_populates="orders_details")

    # def to_read_model(self):
    #     return OrderMenuAssociationSchema(
    #         id=self.id,
    #         order_id=self.order_id,
    #         menu_item_id=self.menu_item_id,
    #         menu_item=self.menu_item,
    #         price=self.price,
    #         quantity=self.quantity,
    #     )

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


# order_menu_association_table = Table(
#     "order_menu_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("orders.id"), nullable=False),
#     Column("menu_item_id", ForeignKey("menu_items.id"), nullable=False),
#     UniqueConstraint("order_id", "menu_item_id", name="idx_unique_order_menu"),
# )
