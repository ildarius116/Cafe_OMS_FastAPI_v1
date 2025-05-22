import contextlib
from typing import Annotated
from fastapi import Path, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.api.dependencies.authentification.users import get_users_db
from src.api.dependencies.authentification.user_manager import get_user_manager
from src.core.cruds.menu_items import get_menu_items_one
from src.core.models import (
    db_helper,
    MenuItemModel,
    OrderMenuAssociation,
    OrderModel,
    User,
)
from src.core.schemas.users import UserRead


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


async def get_user_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    """
    Функция получения элемента меню по id..
    """
    query = select(User).where(User.id == pk)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {pk} not found!",
    )


get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def get_user_manager():
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                yield user_manager
