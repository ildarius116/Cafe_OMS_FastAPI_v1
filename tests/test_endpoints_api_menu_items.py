import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_menu_items(
    async_client: AsyncClient,
    clean_db,
):
    """Тест API - создание элемента Меню"""
    response = await async_client.post(
        url="/api/v1/menu_items/",
        json={
            "name": "Шурпа",
            "price": 111,
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") is not None
    assert data.get("name") == "Шурпа"
    assert data.get("price") == 111


@pytest.mark.asyncio
async def test_get_menu_items_list(
    async_client: AsyncClient,
    clean_db,
    pre_created_menu_items,
):
    """Тест API - получение списка элементов Меню"""
    response = await async_client.get("/api/v1/menu_items/")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pk, st_code",
    [
        (1, 200),
        (2, 200),
        (100, 404),
    ],
)
async def test_get_menu_items_one(
    async_client: AsyncClient,
    pk,
    st_code,
    clean_db,
    pre_created_menu_items,
):
    """Тест API - получение одного конкретного элемента Меню"""
    response = await async_client.get(f"/api/v1/menu_items/{pk}/")
    assert response.status_code == st_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pk, upd_data",
    [
        (
            1,
            {
                "name": "Соус по-сычуаньски",
                "type": "others",
                "price": 1111,
            },
        ),
        (
            2,
            {
                "name": "Компот из урюка",
                "type": "cold drinks",
            },
        ),
        (
            3,
            {
                "price": 777,
            },
        ),
    ],
)
async def test_menu_items_update_partial(
    async_client: AsyncClient,
    test_db_session: AsyncSession,
    pk,
    upd_data,
    clean_db,
    pre_created_menu_items,
):
    """Тест API - частичное обновление элемента Меню"""
    response = await async_client.patch(
        url=f"/api/v1/menu_items/{pk}/",
        json={**upd_data},
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == pk
    if upd_data.get("name"):
        assert data.get("name") == upd_data.get("name")
    if upd_data.get("type"):
        assert data.get("type") == upd_data.get("type")
    if upd_data.get("price"):
        assert data.get("price") == upd_data.get("price")


@pytest.mark.asyncio
async def test_menu_items_update_full(
    async_client: AsyncClient,
    test_db_session: AsyncSession,
    clean_db,
    pre_created_menu_items,
):
    """Тест API - полное обновление элемента Меню"""
    response = await async_client.put(
        url=f"/api/v1/menu_items/1/",
        json={
            "name": "Курица по-пекински",
            "type": "second courses",
            "price": 5555,
        },
    )
    assert response.status_code == 201
    data: dict = response.json()
    assert data.get("id") == 1
    assert data.get("price") == 5555
    assert data.get("type") == "second courses"
    assert data.get("name") == "Курица по-пекински"


@pytest.mark.asyncio
async def test_delete_menu_items(
    async_client: AsyncClient,
    clean_db,
    pre_created_menu_items,
):
    """Тест API - удаление элемента Меню"""
    response = await async_client.delete("/api/v1/menu_items/1/")
    assert response.status_code == 204
