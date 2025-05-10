from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.models import db_helper, OrderModel, OrderMenuAssociation


async def get_order_by_id_with_menu_items_assoc(session: AsyncSession, pk: int):
    query = (
        select(OrderModel)
        .options(
            selectinload(OrderModel.menu_items_details).joinedload(
                OrderMenuAssociation.menu_item
            ),
        )
        .where(OrderModel.id == pk)
        .order_by(OrderModel.id)
    )
    order = await session.scalar(query)
    return order


async def get_order_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderModel:
    """
    Функция получения элемента меню по id..
    """
    result = await get_order_by_id_with_menu_items_assoc(session=session, pk=pk)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {pk} not found!",
    )
