from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from src.api_v1.orders.schemas import (
    OrderBaseSchema,
    OrderSchema,
    OrdersSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)
from src.core.models import OrderModel


async def create_order(
    session: AsyncSession,
    order_in: OrderCreateSchema,
) -> OrderModel:
    print(f"create_order order_in: {order_in}")
    order = OrderModel(**order_in.model_dump())
    print(f"create_order order: {order}")
    order.order_items = []
    # print(f"create_order order: {order}")
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
        .options(selectinload(OrderModel.order_items))
        .order_by(OrderModel.id)
    )
    result: Result = await session.execute(query)
    result = result.scalars().all()
    # result = await session.scalars(query)
    # for res in result:
    #     print(f"get_order_list res: {res}")
    #     print(f"get_order_list res.order_items: {res.order_items}")
    return list(result)


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
