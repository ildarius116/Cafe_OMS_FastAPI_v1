import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.cruds.menu_items import (
    create_menu_item,
    get_menu_items_list,
    update_menu_item,
    delete_menu_item,
)
from src.core.models import MenuItemModel
from src.core.schemas.menu_items import (
    MenuItemCreateSchema,
    MenuItemUpdatePartialSchema,
)


@pytest.mark.asyncio
async def test_create_menu_item(
    clean_db,
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест создания элемента Меню"""

    menu_item: MenuItemModel = await create_menu_item(
        session=test_db_session, menu_item_in=test_menu_items_data[1]
    )

    # проверка
    assert menu_item.id == 1
    assert menu_item.name == "Кофе"
    assert menu_item.price == 60


@pytest.mark.asyncio
async def test_get_menu_items_list(
    clean_db,
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест вывода списка элементов Меню"""

    for test_menu_item in test_menu_items_data:
        await create_menu_item(session=test_db_session, menu_item_in=test_menu_item)
    menu_item_list = await get_menu_items_list(test_db_session)

    # проверка
    assert len(menu_item_list) == 9


@pytest.mark.asyncio
async def test_update_menu_item(
    clean_db,
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест обновления элемента Меню"""

    menu_item: MenuItemModel = await create_menu_item(
        session=test_db_session, menu_item_in=test_menu_items_data[1]
    )
    # проверка текущего состояния
    assert menu_item.id == 1
    assert menu_item.name == "Кофе"
    assert menu_item.price == 60

    order_update_data: MenuItemUpdatePartialSchema = MenuItemUpdatePartialSchema(
        price=55
    )
    menu_item: MenuItemModel = await update_menu_item(
        session=test_db_session,
        menu_item=menu_item,
        item_update=order_update_data,
        partial=True,
    )

    # проверка после внесения изменений
    assert menu_item.id == 1
    assert menu_item.name == "Кофе"
    assert menu_item.price == 55

    order_update_data: MenuItemUpdatePartialSchema = MenuItemUpdatePartialSchema(
        name="Кофе Капучино"
    )
    menu_item: MenuItemModel = await update_menu_item(
        session=test_db_session,
        menu_item=menu_item,
        item_update=order_update_data,
        partial=True,
    )

    # проверка после внесения изменений
    assert menu_item.id == 1
    assert menu_item.name == "Кофе Капучино"
    assert menu_item.price == 55


@pytest.mark.asyncio
async def test_delete_menu_item(
    clean_db,
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест удаления элемента Меню"""

    for test_menu_item in test_menu_items_data:
        await create_menu_item(session=test_db_session, menu_item_in=test_menu_item)
    menu_item_list = await get_menu_items_list(test_db_session)

    # проверка списка до удаления заказа
    assert len(menu_item_list) == 9

    await delete_menu_item(session=test_db_session, menu_item=menu_item_list[0])
    menu_item_list = await get_menu_items_list(test_db_session)

    # проверка списка после удаления заказа
    assert len(menu_item_list) == 8
