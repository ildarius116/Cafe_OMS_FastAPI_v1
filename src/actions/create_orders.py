import asyncio
import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper, OrderModel
from src.core.schemas.orders import OrderCreateSchema

log = logging.getLogger(__name__)


def orders_data() -> list:
    """Функция списка данных для создания заказов"""
    data_list: List[OrderCreateSchema] = [
        OrderCreateSchema(
            table_number=1,
            status="pending",
        ),
        OrderCreateSchema(
            table_number=2,
            status="ready",
        ),
        OrderCreateSchema(
            table_number=3,
            status="paid",
        ),
        OrderCreateSchema(
            table_number=1,
            status="paid",
        ),
        OrderCreateSchema(
            table_number=5,
            status="paid",
        ),
        OrderCreateSchema(
            table_number=8,
            status="ready",
        ),
    ]
    return data_list


async def create_orders(
    orders_data: List[OrderCreateSchema],
    session: AsyncSession,
) -> None:
    """Функция создания заказов"""
    i = 0
    for i, order in enumerate(orders_data):
        order: OrderModel = OrderModel(**order.model_dump())
        session.add(order)
    await session.commit()
    log.warning(f"Created {i+1} orders")


if __name__ == "__main__":
    orders_data = orders_data()
    session = db_helper.get_scoped_session()
    asyncio.run(create_orders(orders_data=orders_data, session=session))
