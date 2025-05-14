from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from src.core.schemas.menu_items import (
    MenuItemCreateSchema,
    MenuItemUpdateSchema,
    MenuItemUpdatePartialSchema,
)
from src.core.models import MenuItemModel


async def create_menu_item(
    session: AsyncSession, menu_item_in: MenuItemCreateSchema
) -> MenuItemModel:
    menu_item = MenuItemModel(**menu_item_in.model_dump())
    session.add(menu_item)
    await session.commit()
    await session.refresh(menu_item)
    return menu_item


async def get_menu_items_one(session: AsyncSession, pk: int) -> MenuItemModel | None:
    print(f"get_menu_item_by_id result: {session}")
    return await session.get(MenuItemModel, pk)


async def get_menu_items_list(session: AsyncSession) -> List[MenuItemModel]:
    query = select(MenuItemModel).order_by(MenuItemModel.id)
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
