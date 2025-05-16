import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.cruds.menu_items import create_menu_item
from src.core.cruds.order_menu_association import (
    add_menu_item_into_order,
    del_menu_item_from_order,
    get_associations_list,
)
from src.core.cruds.orders import create_order
from src.core.dependencies import get_association_by_id
from src.core.models import OrderModel, MenuItemModel, OrderMenuAssociation
from src.core.schemas.menu_items import MenuItemCreateSchema
from src.core.schemas.orders import OrderCreateSchema


@pytest.mark.asyncio
async def test_add_menu_item_into_order(
    clean_db,
    test_db_session: AsyncSession,
    test_orders_data: List[OrderCreateSchema],
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест добавления элемента меню в заказ"""

    order: OrderModel = await create_order(
        session=test_db_session,
        order_in=test_orders_data[1],
    )
    menu_item: MenuItemModel = await create_menu_item(
        session=test_db_session,
        menu_item_in=test_menu_items_data[1],
    )
    order: OrderModel = await add_menu_item_into_order(
        session=test_db_session,
        order=order,
        menu_item=menu_item,
        quantity=3,
    )

    # проверка
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "ready"
    assert order.total_price == 180
    assert order.menu_items_details[0].id == 1
    assert order.menu_items_details[0].menu_item_id == 1
    assert order.menu_items_details[0].price == 180
    assert order.menu_items_details[0].quantity == 3
    assert order.menu_items_details[0].menu_item.name == "Кофе"
    assert order.menu_items_details[0].menu_item.price == 60.0


@pytest.mark.asyncio
async def test_get_associations_list(
    clean_db,
    test_db_session: AsyncSession,
    test_orders_data: List[OrderCreateSchema],
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест получения списка связей m2m "Заказ - элементы Меню" """

    order: OrderModel = await create_order(
        session=test_db_session,
        order_in=test_orders_data[1],
    )
    for test_menu_item in test_menu_items_data:
        menu_item: MenuItemModel = await create_menu_item(
            session=test_db_session,
            menu_item_in=test_menu_item,
        )
        order: OrderModel = await add_menu_item_into_order(
            session=test_db_session,
            order=order,
            menu_item=menu_item,
            quantity=1,
        )

    associations_list: List[OrderMenuAssociation] = await get_associations_list(
        session=test_db_session,
    )

    # проверка
    assert len(associations_list) == 9


@pytest.mark.asyncio
async def test_del_menu_item_from_order(
    clean_db,
    test_db_session: AsyncSession,
    test_orders_data: List[OrderCreateSchema],
    test_menu_items_data: List[MenuItemCreateSchema],
):
    """Тест удаления элемента Меню из заказа"""

    order: OrderModel = await create_order(
        session=test_db_session,
        order_in=test_orders_data[1],
    )
    for test_menu_item in test_menu_items_data:
        menu_item: MenuItemModel = await create_menu_item(
            session=test_db_session,
            menu_item_in=test_menu_item,
        )
        await add_menu_item_into_order(
            session=test_db_session,
            order=order,
            menu_item=menu_item,
            quantity=1,
        )
    associations_list: List[OrderMenuAssociation] = await get_associations_list(
        session=test_db_session,
    )

    # проверка до удаления элемента Меню
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "ready"
    assert order.total_price == 280
    assert len(associations_list) == 9

    association: OrderMenuAssociation = await get_association_by_id(
        pk=order.menu_items_details[0].menu_item_id,
        session=test_db_session,
    )
    await del_menu_item_from_order(
        session=test_db_session,
        association=association,
    )
    associations_list: List[OrderMenuAssociation] = await get_associations_list(
        session=test_db_session,
    )

    # проверка после удаления элемента Меню
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "ready"
    assert order.total_price == 270
    assert len(associations_list) == 8
