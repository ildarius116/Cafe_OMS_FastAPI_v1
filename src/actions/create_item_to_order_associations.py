import asyncio
import logging
from typing import Annotated
from fastapi import Depends, Path, HTTPException, status
from random import randint
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.menu_items import get_menu_items_one
from src.core.cruds.orders import get_order_list
from src.core.models import (
    db_helper,
    OrderMenuAssociation,
    MenuItemModel,
)
from src.core.schemas.order_menu_association import OrderMenuAssociationAddSchema

log = logging.getLogger(__name__)


async def get_menu_item_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MenuItemModel:
    """
    Функция получения элемента меню по id.
    """
    result = await get_menu_items_one(session=session, pk=pk)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {pk} not found!",
    )


async def create_associations(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """Функция с предсозданными ассоциациями"""
    i = j = 0
    orders = await get_order_list(session=session)
    for i, order in enumerate(orders):
        rnd_menu_item_qty = randint(1, 5)
        menu_item_id_set = set()
        for j in range(rnd_menu_item_qty):
            rnd_qty = randint(1, 5)
            while True:
                rnd_menu_item_id = randint(1, 16)
                if rnd_menu_item_id not in menu_item_id_set:
                    menu_item_id_set.add(rnd_menu_item_id)

                    association = OrderMenuAssociationAddSchema(
                        menu_item_id=rnd_menu_item_id,
                        quantity=rnd_qty,
                    )
                    menu_item = await get_menu_item_by_id(
                        session=session,
                        pk=rnd_menu_item_id,
                    )

                    price = association.quantity * menu_item.price
                    order.menu_items_details.append(
                        OrderMenuAssociation(
                            menu_item=menu_item,
                            quantity=rnd_qty,
                            price=price,
                        )
                    )
                    order.total_price += price
                    break

        log.warning(f"Created {j+1} associations for {i+1}-order")
    await session.commit()
    log.warning(f"Modifies {i+1} orders")


if __name__ == "__main__":
    session = db_helper.get_scoped_session()
    asyncio.run(create_associations(session=session))
