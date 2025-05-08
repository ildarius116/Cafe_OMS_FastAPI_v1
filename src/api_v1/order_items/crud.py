from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from src.api_v1.menu_items.dependencies import get_menu_item_by_id
from src.api_v1.order_items.schemas import (
    OrderItemSchema,
    OrderItemUpdateSchema,
    OrderItemUpdatePartialSchema,
    OrderItemCreateSchema,
)
from src.core.models import OrderItemModel, OrderModel, MenuItemModel


async def create_order_item(
    session: AsyncSession,
    order_item_in: OrderItemCreateSchema,
) -> OrderItemModel:
    menu_item_id = order_item_in.menu_item_id
    order_item = OrderItemModel(**order_item_in.model_dump())
    menu_item: MenuItemModel = await get_menu_item_by_id(
        pk=menu_item_id, session=session
    )
    order_item.price = order_item.quantity * menu_item.price
    session.add(order_item)
    await session.commit()
    await session.refresh(order_item)
    return order_item


async def get_order_item_one(
    session: AsyncSession,
    pk: int,
) -> OrderItemModel | None:
    return await session.get(OrderItemModel, pk)


async def get_order_item_list(session: AsyncSession) -> List[OrderItemModel]:
    query = select(OrderItemModel).order_by(OrderItemModel.id)
    result: Result = await session.execute(query)
    result = result.scalars().all()
    return list(result)


async def update_order_item(
    session: AsyncSession,
    order_item: OrderItemModel,
    order_item_update: OrderItemUpdateSchema | OrderItemUpdatePartialSchema,
    partial: bool = False,
) -> OrderItemModel:
    for key, value in order_item_update.model_dump(exclude_unset=partial).items():
        setattr(order_item, key, value)
    await session.commit()
    await session.refresh(order_item)
    return order_item


async def delete_order_item(
    session: AsyncSession,
    order_item: OrderItemModel,
) -> None:
    await session.delete(order_item)
    await session.commit()
