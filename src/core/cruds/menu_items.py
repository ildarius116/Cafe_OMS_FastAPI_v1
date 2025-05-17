from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from src.core.models import MenuItemModel
from src.core.schemas.menu_items import (
    MenuItemCreateSchema,
    MenuItemUpdateSchema,
    MenuItemUpdatePartialSchema,
)


async def create_menu_item(
    session: AsyncSession, menu_item_in: MenuItemCreateSchema
) -> MenuItemModel:
    menu_item = MenuItemModel(**menu_item_in.model_dump())
    session.add(menu_item)
    await session.commit()
    await session.refresh(menu_item)
    return menu_item


async def get_menu_items_one(session: AsyncSession, pk: int) -> MenuItemModel | None:
    return await session.get(MenuItemModel, pk)


async def get_menu_items_list(session: AsyncSession, fltr=None) -> List[MenuItemModel]:
    if not fltr:
        fltr = {}
    query = select(MenuItemModel)
    name = fltr.get("name")
    if name:
        query = query.where(MenuItemModel.name.like(f"{name}%"))
    type = fltr.get("type")
    if type:
        query = query.where(MenuItemModel.type == type)
    query = query.order_by(MenuItemModel.id)
    result: Result = await session.execute(query)
    result = result.scalars().all()
    return list(result)


async def update_menu_item(
    session: AsyncSession,
    menu_item: MenuItemModel,
    item_update: MenuItemUpdateSchema | MenuItemUpdatePartialSchema,
    partial: bool = False,
) -> MenuItemModel:
    for key, value in item_update.model_dump(exclude_unset=partial).items():
        setattr(menu_item, key, value)
    await session.commit()
    await session.refresh(menu_item)
    return menu_item


async def delete_menu_item(
    session: AsyncSession,
    menu_item: MenuItemModel,
) -> None:
    await session.delete(menu_item)
    await session.commit()
