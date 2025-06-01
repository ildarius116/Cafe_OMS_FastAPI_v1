from typing import Annotated
from fastapi import Path, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.core.cruds.menu_items import get_menu_items_one
from src.core.models import (
    db_helper,
    MenuItemModel,
    OrderModel,
    OrderMenuAssociation,
    User,
    Role,
    Permission,
)


async def get_menu_item_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MenuItemModel:
    """Функция получения элемента меню по id."""
    result = await get_menu_items_one(session=session, pk=pk)
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
    """Функция получения заказа по id."""
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


async def get_association_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderMenuAssociation:
    """Функция получения элемента меню по id."""
    query = select(OrderMenuAssociation).where(OrderMenuAssociation.id == pk)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Association {pk} not found!",
    )


async def get_user_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    """Функция получения пользователя по id."""

    query = (
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.permissions),
        )
        .where(User.id == pk)
    )
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {pk} not found!",
    )


async def get_user_by_email(
    email: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    """Функция получения пользователя по email."""
    query = (
        select(User)
        .options(
            selectinload(User.roles),
        )
        .where(User.email == email)
        .order_by(User.id)
    )
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {email} not found!",
    )


async def get_role_by_id(
    role_pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Role:
    """Функция получения роли по id."""
    query = (
        select(Role)
        .options(
            selectinload(Role.permissions),
        )
        .where(Role.id == role_pk)
        .order_by(Role.id)
    )
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Role {role_pk} not found!",
    )


async def get_permission_by_id(
    perm_pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Permission:
    """Функция получения разрешения по id."""
    query = select(Permission).where(Permission.id == perm_pk)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Permission {perm_pk} not found!",
    )
