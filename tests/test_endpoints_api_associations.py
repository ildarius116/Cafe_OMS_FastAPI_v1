import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_associations_list(
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
        url=f"/api/v1/association/{2}/",
        json={
            "menu_item_id": 4,
            "quantity": 3,
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == 2
    assert data.get("menu_items_details", {})[0].get("order_id") == 2
    assert data.get("menu_items_details", {})[0].get("menu_item_id") == 4
    assert data.get("menu_items_details", {})[0].get("quantity") == 3


@pytest.mark.asyncio
async def test_delete_association_from_order(
    async_client: AsyncClient,
):
    """Тест API - удаление элемента Меню из заказа"""
    response = await async_client.delete("/api/v1/association/9/")
    assert response.status_code == 204
