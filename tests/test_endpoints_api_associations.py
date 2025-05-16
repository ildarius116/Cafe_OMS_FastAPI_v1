import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_associations_get_list(
    async_client: AsyncClient,
):
    """Тест API - получение списка связей элементов Меню и заказов"""
    response = await async_client.get("/api/v1/association/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_association_add_into_order(
    async_client: AsyncClient,
):
    """Тест API - добавление элемента Меню в заказ"""

    response = await async_client.post(
        url="/api/v1/orders/",
        json={
            "table_number": 1,
            "status": "pending",
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        url="/api/v1/menu_items/",
        json={
            "name": "Шурпа",
            "price": 111,
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        url=f"/api/v1/association/1/",
        json={
            "menu_item_id": 1,
            "quantity": 3,
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == 1
    assert data.get("menu_items_details", {})[0].get("order_id") == 1
    assert data.get("menu_items_details", {})[0].get("menu_item_id") == 1
    assert data.get("menu_items_details", {})[0].get("quantity") == 3


@pytest.mark.asyncio
async def test_association_delete_from_order(
    async_client: AsyncClient,
):
    """Тест API - удаление элемента Меню из заказа"""
    response = await async_client.delete("/api/v1/association/1/")
    await async_client.delete("/api/v1/orders/1/")
    await async_client.delete("/api/v1/menu_items/1/")

    assert response.status_code == 204
