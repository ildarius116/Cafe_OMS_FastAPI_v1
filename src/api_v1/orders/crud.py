from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.api_v1.orders.schemas import (
    OrderBaseSchema,
    OrderSchema,
    OrdersSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)
from src.core.models import OrderModel, OrderMenuAssociation


async def create_order(
    session: AsyncSession,
    order_in: OrderCreateSchema,
) -> OrderModel:
    order = OrderModel(**order_in.model_dump())
    print(f"create_order order: {order}")
    # order.order_items = []
    session.add(order)
    await session.commit()
    print(f"create_order order: {order}")
    return order


async def get_order_one(
    session: AsyncSession,
    pk: int,
) -> OrderModel | None:
    return await session.get(OrderModel, pk)


async def get_order_list(session: AsyncSession) -> List[OrderModel]:
    query = (
        select(OrderModel)
        .options(
            selectinload(OrderModel.menu_items_details).joinedload(
                OrderMenuAssociation.menu_item
            ),
        )
        .order_by(OrderModel.id)
    )
    orders = await session.scalars(query)
    # orders = [order.to_read_model() for order in orders]
    print(f"\n get_order_list orders: {orders}")
    return list(orders)


async def update_order(
    session: AsyncSession,
    order: OrderModel,
    order_update: OrderUpdateSchema | OrderUpdatePartialSchema,
    partial: bool = False,
) -> OrderModel:
    for key, value in order_update.model_dump(exclude_unset=partial).items():
        setattr(order, key, value)
    await session.commit()
    await session.refresh(order)
    return order


async def delete_order(
    session: AsyncSession,
    order: OrderModel,
) -> None:
    await session.delete(order)
    await session.commit()
