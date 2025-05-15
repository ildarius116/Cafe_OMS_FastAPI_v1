from typing import List

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from src.core.config import settings
from src.core.models import Base, OrderModel, MenuItemModel, OrderMenuAssociation
from src.core.schemas.menu_items import MenuItemCreateSchema
from src.core.schemas.orders import OrderCreateSchema
from src.main import app

engine: AsyncEngine = create_async_engine(
    url=settings.db_test_url,
    poolclass=NullPool,
    echo=settings.debug,
    # echo=settings.debug,
)

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest_asyncio.fixture(scope="session")
async def test_db():
    """
    Функция-фикстура инициализации и очистка тестовой БД
    """

    async with engine.begin() as conn:
        print("BEFORE CREATE !!!!!!!!!!!!!!!!!")
        await conn.run_sync(Base.metadata.create_all)
        print("AFTER CREATE !!!!!!!!!!!!!!!!!")
    yield engine
    async with engine.begin() as conn:
        print("BEFORE DROP !!!!!!!!!!!!!!!!!")
        await conn.run_sync(Base.metadata.drop_all)
        print("AFTER DROP !!!!!!!!!!!!!!!!!")


@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_db) -> AsyncSession:
    """
    Функция-фикстура асинхронной сессии
    """
    async with async_session() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app),
        base_url="http://localhost",
    )


@pytest_asyncio.fixture
async def clean_db(test_db_session: AsyncSession):
    """
    Функция-фикстура очистки БД перед тестом
    """
    await test_db_session.execute(delete(OrderModel))
    await test_db_session.execute(delete(MenuItemModel))
    await test_db_session.execute(delete(OrderMenuAssociation))
    await test_db_session.commit()
    yield


@pytest_asyncio.fixture
async def test_orders():
    """
    Функция-фикстура
    """
    data_list: List[OrderCreateSchema] = [
        OrderCreateSchema(
            table_number=1,
            status="pending",
        ),
        OrderCreateSchema(
            table_number=2,
            status="ready",
        ),
        OrderCreateSchema(
            table_number=3,
            status="paid",
        ),
        OrderCreateSchema(
            table_number=1,
            status="paid",
        ),
    ]

    return data_list


@pytest_asyncio.fixture
async def test_menu_items():
    """
    Функция-фикстура
    """
    data_list = [
        MenuItemCreateSchema(
            name="Чай",
            price=10,
        ),
        MenuItemCreateSchema(
            name="Кофе",
            price=60,
        ),
        MenuItemCreateSchema(
            name="Каша Гречневая",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Ячневая",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Молочная",
            price=30,
        ),
        MenuItemCreateSchema(
            name="Яичница (2шт.)",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Сосиски (2шт.)",
            price=35,
        ),
        MenuItemCreateSchema(
            name="Суп Гороховый",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Стейк Говяжий",
            price=55,
        ),
    ]

    return data_list


@pytest_asyncio.fixture
async def created_orders(
    test_db_session: AsyncSession,
    test_orders: List[OrderCreateSchema],
) -> None:
    for test_order in test_orders:
        order: OrderModel = OrderModel(**test_order.model_dump())
        test_db_session.add(order)
    await test_db_session.commit()
    # await test_db_session.refresh(order)
    # return order
