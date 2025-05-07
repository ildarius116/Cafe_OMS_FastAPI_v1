from sqlalchemy import String, TIMESTAMP, func, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

from src.orders.schemas import OrderItemSchema, OrderBaseSchema
from src.core.models import Base


class OrderModel(Base):
    __tablename__ = "order"

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

    # order_items: Mapped[List["OrderItemModel"]] = relationship(
    #     back_populates="order", cascade="all, delete-orphan"
    # )

    def calculate_total(self) -> float:
        return sum(item.price for item in self.order_items.all()) if self.pk else 0

    def save(self, *args, **kwargs):
        if self.pk:
            self.total_price = self.calculate_total()
        return super().save(*args, **kwargs)

    def to_read_model(self):
        return OrderBaseSchema(
            id=self.id,
            table_number=self.table_number,
            order_items=(
                [item.to_read_model() for item in self.order_items]
                if self.order_items
                else []
            ),
            total_price=self.total_price,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __repr__(self):
        return (
            f"Order(id={self.id}, table_number={self.table_number}, "
            f"total_price={self.total_price}, status={self.status}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )


class OrderItemModel(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))
    # price: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), name="Цена")
    price: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    quantity: Mapped[int] = mapped_column(default=1)  # Добавляем quantity

    # Связи
    # order: Mapped["OrderModel"] = relationship(back_populates="order_items")
    # menu_item: Mapped["MenuItemModel"] = relationship(back_populates="order_items")

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
        self.order.save()

    def to_read_model(self):
        return OrderItemSchema(
            id=self.id,
            order_id=self.order_id,
            menu_item_id=self.menu_item_id,
            price=self.price,
            quantity=self.quantity,
            # menu_item=self.menu_item.to_read_model() if self.menu_item else None,
        )

    def __repr__(self) -> str:
        return (
            f"<Order_item(id={self.id}, "
            f"order_id={self.order_id}, "
            f"menu_item_id={self.menu_item_id}, "
            f"price={self.price})>"
        )
