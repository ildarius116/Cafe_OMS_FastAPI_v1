from sqlalchemy import String, TIMESTAMP, func, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from datetime import datetime

from src.core.models import Base
from src.core.models.mixin import IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models.order_menu_association import OrderMenuAssociation


class OrderModel(Base, IdIntPkMixin):
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

    menu_items_details: Mapped[List["OrderMenuAssociation"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"Order(id={self.id}, "
            f"Order(order_items={self.menu_items_details}, "
            f"table_number={self.table_number}, "
            f"total_price={self.total_price}, "
            f"status={self.status}, "
            f"created_at={getattr(self, 'created_at', None)}, "
            f"updated_at={getattr(self, 'updated_at', None)}"
        )
