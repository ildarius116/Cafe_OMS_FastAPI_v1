from sqlalchemy import String, TIMESTAMP, func, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from src.core.models import Base

if TYPE_CHECKING:
    from src.core.models.order_menu_association import OrderMenuAssociation


class OrderModel(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'ready', 'paid')", name="check_status_valid"
        ),
    )

    table_number: Mapped[int]
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    status: Mapped[str] = mapped_column(String(10), default="pending")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    # menu_items: Mapped[List["MenuItemModel"]] = relationship(
    #     secondary="order_menu_association",
    #     back_populates="orders",
    # )
    menu_items_details: Mapped[List["OrderMenuAssociation"]] = relationship(
        back_populates="order",
    )

    # def calculate_total(self) -> float:
    #     return sum(item.price for item in self.order_items.all()) if self.pk else 0

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.total_price = self.calculate_total()
    #     return super().save(*args, **kwargs)

    # def to_read_model(self):
    #     return OrderSchema(
    #         id=self.id,
    #         table_number=self.table_number,
    #         menu_items_details=(
    #             [item.to_read_model() for item in self.menu_items_details]
    #             if self.menu_items_details
    #             else []
    #         ),
    #         total_price=self.total_price,
    #         status=self.status,
    #         created_at=self.created_at,
    #         updated_at=self.updated_at,
    #     )

    def __repr__(self):
        return (
            f"Order(id={self.id}, "
            f"Order(order_items={self.menu_items_details}, "
            f"table_number={self.table_number}, "
            f"total_price={self.total_price}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )
