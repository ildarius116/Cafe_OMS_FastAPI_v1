import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from src.core.cruds.orders import create_order, get_order_list
from src.core.models import OrderModel
from src.core.schemas.orders import OrderCreateSchema
from src.main import app


@pytest.mark.asyncio
async def test_create_order(
    test_db_session: AsyncSession,
    clean_db,
):
    """Тест создания заказа"""

    test_data = OrderCreateSchema(table_number=1, status="ready")
    result: OrderModel = await create_order(test_db_session, test_data)

    # проверка
    assert result.id == 1
    assert result.table_number == 1
    assert result.status == "ready"
    assert result.total_price == 0
    assert result.created_at is not None
    assert result.updated_at is not None


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
        await create_order(test_db_session, test_order)
    orders_list = await get_order_list(test_db_session, fltr)

    # проверка
    assert len(orders_list) == qty
