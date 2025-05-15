import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from src.core.cruds.orders import create_order, get_order_list, update_order
from src.core.models import OrderModel
from src.core.schemas.orders import (
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
)
from src.main import app


@pytest.mark.asyncio
async def test_create_order(
    test_db_session: AsyncSession,
    clean_db,
    test_orders: List[OrderCreateSchema],
):
    """Тест создания заказа"""

    order: OrderModel = await create_order(
        session=test_db_session, order_in=test_orders[1]
    )

    # проверка
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "ready"
    assert order.total_price == 0
    assert order.created_at is not None
    assert order.updated_at is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fltr, qty",
    [
        (None, 4),
        ({"status": "paid"}, 2),
        ({"table_number": 1}, 2),
    ],
)
async def test_get_order_list(
    test_db_session: AsyncSession,
    clean_db,
    test_orders: List[OrderCreateSchema],
    fltr,
    qty,
):
    """Тест вывода списка заказов с применением фильтрации"""

    for test_order in test_orders:
        await create_order(session=test_db_session, order_in=test_order)
    orders_list = await get_order_list(test_db_session, fltr)

    # проверка
    assert len(orders_list) == qty


@pytest.mark.asyncio
async def test_update_order(
    test_db_session: AsyncSession,
    clean_db,
    test_orders: List[OrderCreateSchema],
):
    """Тест обновления заказа"""

    order: OrderModel = await create_order(
        session=test_db_session, order_in=test_orders[1]
    )
    # проверка текущего состояния
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "ready"

    order_update_data: OrderUpdatePartialSchema = OrderUpdatePartialSchema(
        status="paid"
    )
    order: OrderModel = await update_order(
        session=test_db_session,
        order=order,
        order_update=order_update_data,
        partial=True,
    )

    # проверка после внесения изменений
    assert order.id == 1
    assert order.table_number == 2
    assert order.status == "paid"
