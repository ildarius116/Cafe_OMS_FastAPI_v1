from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.menu_items.crud import get_menu_items_one
from src.api_v1.order_items.crud import get_order_item_one
from src.api_v1.orders.crud import get_order_one
from src.core.models import db_helper, OrderModel, MenuItemModel, OrderItemModel


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


async def get_order_item_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderItemModel:
    """
    Функция получения элемента меню по id..
    """
    result = await get_order_item_one(session=session, pk=pk)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {pk} not found!",
    )


async def get_order_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderModel:
    """
    Функция получения элемента меню по id..
    """
    result = await get_order_one(session=session, pk=pk)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu item {pk} not found!",
    )
