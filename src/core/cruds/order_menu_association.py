from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.orders import update_order
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
    order_update = OrderUpdatePartialSchema(order_update=order.total_price + price)
    order = await update_order(
        session=session, order=order, order_update=order_update, partial=True
    )
    await session.commit()
    return await session.get(OrderModel, order.id)


async def del_menu_item_from_order(
    session: AsyncSession,
    association: OrderMenuAssociation,
) -> None:
    await session.delete(association)
    await session.commit()
