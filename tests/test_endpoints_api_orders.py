import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_order_list(
    async_client: AsyncClient,
):
    """Тест API - получение списка заказов"""
    response = await async_client.get("/api/v1/orders/")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pk, st_code",
    [
        (1, 200),
        (2, 200),
        (5, 404),
    ],
)
async def test_get_order_one(
    async_client: AsyncClient,
    pk,
    st_code,
):
    """Тест API - получение одного конкретного заказа"""
    response = await async_client.get(f"/api/v1/orders/{pk}/")
    assert response.status_code == st_code


@pytest.mark.asyncio
async def test_create_order(
    async_client: AsyncClient,
):
    """Тест API - создание заказа"""
    response = await async_client.post(
        url="/api/v1/orders/",
        json={
            "table_number": 1,
            "status": "pending",
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") is not None
    assert data.get("table_number") == 1
    assert data.get("status") == "pending"
    assert data.get("total_price") == 0
    assert data.get("created_at") is not None
    assert data.get("updated_at") is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pk, upd_data",
    [
        (
            1,
            {
                "table_number": 15,
                "status": "ready",
                "total_price": 50,
            },
        ),
        (
            2,
            {
                "table_number": 10,
                "total_price": 100,
            },
        ),
        (
            4,
            {
                "status": "paid",
            },
        ),
    ],
)
async def test_order_update_partial(
    async_client: AsyncClient,
    test_db_session: AsyncSession,
    pk,
    upd_data,
):
    """Тест API - частичное обновление заказа"""
    response = await async_client.patch(
        url=f"/api/v1/orders/{pk}/",
        json={**upd_data},
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == pk
    if upd_data.get("table_number"):
        assert data.get("table_number") == upd_data.get("table_number")
    if upd_data.get("status"):
        assert data.get("status") == upd_data.get("status")
    if upd_data.get("total_price"):
        assert data.get("total_price") == upd_data.get("total_price")


@pytest.mark.asyncio
async def test_order_update_full(
    async_client: AsyncClient,
    test_db_session: AsyncSession,
    clean_db,
):
    """Тест API - полное обновление заказа"""
    response = await async_client.put(
        url=f"/api/v1/orders/{2}/",
        json={
            "table_number": 15,
            "status": "ready",
            "menu_items_details": [],
            "total_price": 50,
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == 2
    assert data.get("table_number") == 15
    assert data.get("status") == "ready"
    assert data.get("total_price") == 50


@pytest.mark.asyncio
async def test_delete_order(
    async_client: AsyncClient,
):
    """Тест API - удаление заказа"""
    response = await async_client.delete("/api/v1/orders/4/")
    assert response.status_code == 204
