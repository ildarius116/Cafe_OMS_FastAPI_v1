import asyncio
import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import (
    db_helper,
    MenuItemModel,
)
from src.core.schemas.menu_items import MenuItemCreateSchema

log = logging.getLogger(__name__)


def menu_items_data():
    """Функция списка данных для создания элементов Меню"""
    data_list: List[MenuItemCreateSchema] = [
        MenuItemCreateSchema(
            name="Компот",
            type="cold drinks",
            price=10,
        ),
        MenuItemCreateSchema(
            name="Сок",
            type="cold drinks",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Чай",
            type="hot drinks",
            price=10,
        ),
        MenuItemCreateSchema(
            name="Кофе",
            type="hot drinks",
            price=60,
        ),
        MenuItemCreateSchema(
            name="Каша Гречневая",
            type="garnishes",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Ячневая",
            type="garnishes",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Молочная",
            type="garnishes",
            price=30,
        ),
        MenuItemCreateSchema(
            name="Каша Гороховая",
            type="garnishes",
            price=30,
        ),
        MenuItemCreateSchema(
            name="Суп Гороховый",
            type="first courses",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Суп Лапша",
            type="first courses",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Суп Харчо",
            type="first courses",
            price=30,
        ),
        MenuItemCreateSchema(
            name="Яичница (2шт.)",
            type="second courses",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Сосиски (2шт.)",
            type="second courses",
            price=35,
        ),
        MenuItemCreateSchema(
            name="Купаты (2шт.)",
            type="second courses",
            price=55,
        ),
        MenuItemCreateSchema(
            name="Стейк Говяжий",
            type="second courses",
            price=55,
        ),
        MenuItemCreateSchema(
            name="Котлета Говяжья",
            type="second courses",
            price=35,
        ),
        MenuItemCreateSchema(
            name="Котлета Куриная",
            type="second courses",
            price=30,
        ),
    ]
    return data_list


async def create_menu_items(
    menu_items_data: List[MenuItemCreateSchema],
    session: AsyncSession,
) -> None:
    """Функция с предсозданными элементами Меню"""
    i = 0
    for i, menu_items in enumerate(menu_items_data):
        menu_item: MenuItemModel = MenuItemModel(**menu_items.model_dump())
        session.add(menu_item)
    await session.commit()
    log.warning(f"Created {i+1} menu items")


if __name__ == "__main__":
    menu_items_data = menu_items_data()
    session = db_helper.get_scoped_session()
    asyncio.run(create_menu_items(menu_items_data=menu_items_data, session=session))
