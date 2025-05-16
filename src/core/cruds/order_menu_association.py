from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.orders import get_order_one
from src.core.dependencies import get_order_by_id
from src.core.models import OrderModel, OrderMenuAssociation, MenuItemModel


async def get_associations_list(session: AsyncSession) -> List[OrderMenuAssociation]:
    query = select(OrderMenuAssociation).order_by(OrderMenuAssociation.id)
    result = await session.scalars(query)
    return list(result)


async def add_menu_item_into_order(
    session: AsyncSession,
    order: OrderModel,
    menu_item: MenuItemModel,
    quantity: int,
) -> OrderModel | None:
    price = quantity * menu_item.price
    order_id = order.id
    order.menu_items_details.append(
        OrderMenuAssociation(
            menu_item=menu_item,
            quantity=quantity,
            price=price,
        )
    )
    order.total_price += price
    await session.commit()
    order = await get_order_by_id(session=session, pk=order_id)
    return order


async def del_menu_item_from_order(
    session: AsyncSession,
    association: OrderMenuAssociation,
) -> int:
    order_id = association.order_id
    item_price = association.price
    await session.delete(association)
    order = await get_order_one(session=session, pk=order_id)
    order.total_price -= item_price
    await session.commit()
    return order_id
