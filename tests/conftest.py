from typing import List
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from src.core.config import settings
from src.core.models import (
    Base,
    db_helper,
    DatabaseHelper,
    OrderModel,
    MenuItemModel,
    OrderMenuAssociation,
)
from src.core.schemas.menu_items import MenuItemCreateSchema
from src.core.schemas.orders import OrderCreateSchema
from src.main import app


def pytest_configure(config):
    config.option.asyncio_default_fixture_loop_scope = "function"


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Переопределяем event_loop для session scope"""
    import asyncio

    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


test_db_helper = DatabaseHelper(
    url=settings.db_test_url,
    echo=settings.debug,
)

engine: AsyncEngine = create_async_engine(
    url=settings.db_test_url,
    poolclass=NullPool,
    echo=False,
    # echo=settings.debug,
)


async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_db():
    """
    Функция-фикстура инициализации и очистка тестовой БД
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_db_session(test_db) -> AsyncSession:
    """
    Функция-фикстура асинхронной сессии
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def clean_db(test_db_session: AsyncSession):
    """
    Функция-фикстура очистки БД перед тестом
    """
    for table in reversed(Base.metadata.sorted_tables):
        await test_db_session.execute(table.delete())
    await test_db_session.commit()
    yield


@pytest_asyncio.fixture
async def test_app():
    app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_app) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(test_app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_orders_data():
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
async def test_menu_items_data():
    """
    Функция-фикстура
    """
    data_list: List[MenuItemCreateSchema] = [
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
async def pre_created_orders(
    test_db_session: AsyncSession,
    test_orders_data: List[OrderCreateSchema],
) -> None:
    for test_order in test_orders_data:
        order: OrderModel = OrderModel(**test_order.model_dump())
        test_db_session.add(order)
    await test_db_session.commit()


@pytest_asyncio.fixture
async def pre_created_menu_items(
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
) -> None:
    for test_menu_items in test_menu_items_data:
        menu_item: MenuItemModel = MenuItemModel(**test_menu_items.model_dump())
        test_db_session.add(menu_item)
    await test_db_session.commit()
