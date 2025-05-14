from typing import List, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.orders import update_order, get_order_one
from src.core.models import OrderModel, OrderMenuAssociation, MenuItemModel
from src.core.schemas.orders import OrderUpdatePartialSchema


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
    order.menu_items_details.append(
        OrderMenuAssociation(
            menu_item=menu_item,
            quantity=quantity,
            price=price,
        )
    )
    order.total_price += price
    await session.commit()
    return await session.get(OrderModel, order.id)


async def del_menu_item_from_order(
    session: AsyncSession,
    association: OrderMenuAssociation,
) -> Any:
    order_id = association.order_id
    item_price = association.price
    await session.delete(association)
    order = await get_order_one(session=session, pk=order_id)
    order.total_price -= item_price
    await session.commit()
    return order_id
