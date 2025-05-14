from typing import Annotated
from fastapi import Path, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.core.cruds.menu_items import get_menu_items_one
from src.core.models import db_helper, MenuItemModel, OrderMenuAssociation, OrderModel


async def get_menu_item_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MenuItemModel:
    """
    Функция получения элемента меню по id..
    """
    result = await get_menu_items_one(session=session, pk=pk)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {pk} not found!",
    )


async def get_association_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderMenuAssociation:
    """
    Функция получения элемента меню по id..
    """
    query = select(OrderMenuAssociation).where(OrderMenuAssociation.id == pk)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Association {pk} not found!",
    )


async def get_order_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderModel:
    """
    Функция получения заказа по id.
    """
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
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {pk} not found!",
    )
