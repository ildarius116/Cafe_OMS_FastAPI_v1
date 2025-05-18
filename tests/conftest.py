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
from src.core.dependencies import get_order_by_id, get_menu_item_by_id
from src.core.models import (
    Base,
    db_helper,
    DatabaseHelper,
    OrderModel,
    MenuItemModel,
    OrderMenuAssociation,
)
from src.core.schemas.menu_items import MenuItemCreateSchema
from src.core.schemas.order_menu_association import OrderMenuAssociationAddSchema
from src.core.schemas.orders import OrderCreateSchema
from src.main import app


def pytest_configure(config):
    config.option.asyncio_default_fixture_loop_scope = "function"


test_db_helper = DatabaseHelper(
    url=settings.db.db_test_url,
    echo=settings.debug,
)

engine: AsyncEngine = create_async_engine(
    url=settings.db.db_test_url,
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


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_db_init():
    """Фикстура инициализации и очистка тестовой БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_db_session(test_db_init) -> AsyncSession:
    """Фикстура асинхронной сессии"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def clean_db(test_db_session: AsyncSession):
    """Фикстура очистки БД перед тестом"""
    for table in reversed(Base.metadata.sorted_tables):
        await test_db_session.execute(table.delete())
    await test_db_session.commit()
    yield


@pytest_asyncio.fixture
async def test_app():
    """Фикстура подмены приложения под тесты"""

    app.dependency_overrides[db_helper.session_dependency] = (
        test_db_helper.session_dependency
    )
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_app) -> AsyncClient:
    """Фикстура тестового клиента"""
    async with AsyncClient(
        transport=ASGITransport(test_app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_orders_data():
    """Фикстура списка данных для создания заказов"""
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
    """Фикстура списка данных для создания элементов Меню"""
    data_list: List[MenuItemCreateSchema] = [
        MenuItemCreateSchema(
            name="Чай",
            type="hot drinks",
            price=10,
        ),
        MenuItemCreateSchema(
            name="Кофе",
            type="hot drinks",
            price=60,
        ),
        MenuItemCreateSchema(
            name="Каша Гречневая",
            type="garnishes",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Ячневая",
            type="garnishes",
            price=20,
        ),
        MenuItemCreateSchema(
            name="Каша Молочная",
            type="garnishes",
            price=30,
        ),
        MenuItemCreateSchema(
            name="Яичница (2шт.)",
            type="second courses",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Сосиски (2шт.)",
            type="second courses",
            price=35,
        ),
        MenuItemCreateSchema(
            name="Суп Гороховый",
            type="first courses",
            price=25,
        ),
        MenuItemCreateSchema(
            name="Стейк Говяжий",
            type="second courses",
            price=55,
        ),
    ]
    return data_list


@pytest_asyncio.fixture
async def test_association_data():
    """Фикстура списка данных для m2m связей между таблицами"""
    data_list: List[OrderMenuAssociationAddSchema] = [
        OrderMenuAssociationAddSchema(
            menu_item_id=1,
            quantity=1,
        ),
        OrderMenuAssociationAddSchema(
            menu_item_id=2,
            quantity=5,
        ),
        OrderMenuAssociationAddSchema(
            menu_item_id=3,
            quantity=4,
        ),
        OrderMenuAssociationAddSchema(
            menu_item_id=4,
            quantity=2,
        ),
    ]
    return data_list


@pytest_asyncio.fixture
async def pre_created_orders(
    test_db_session: AsyncSession,
    test_orders_data: List[OrderCreateSchema],
) -> None:
    """Фикстура с предсозданными заказами"""
    for test_order in test_orders_data:
        order: OrderModel = OrderModel(**test_order.model_dump())
        test_db_session.add(order)
    await test_db_session.commit()


@pytest_asyncio.fixture
async def pre_created_menu_items(
    test_db_session: AsyncSession,
    test_menu_items_data: List[MenuItemCreateSchema],
) -> None:
    """Фикстура с предсозданными элементами Меню"""
    for test_menu_items in test_menu_items_data:
        menu_item: MenuItemModel = MenuItemModel(**test_menu_items.model_dump())
        test_db_session.add(menu_item)
    await test_db_session.commit()


@pytest_asyncio.fixture
async def pre_created_associations(
    test_db_session: AsyncSession,
    test_association_data: List[OrderMenuAssociationAddSchema],
    pre_created_orders,
    pre_created_menu_items,
) -> None:
    """Фикстура с предсозданными ассоциациями"""

    for i, association in enumerate(test_association_data):
        order = await get_order_by_id(session=test_db_session, pk=i + 1)
        menu_item = await get_menu_item_by_id(
            session=test_db_session, pk=association.menu_item_id
        )
        price = association.quantity * menu_item.price
        order.menu_items_details.append(
            OrderMenuAssociation(
                menu_item=menu_item,
                quantity=association.quantity,
                price=price,
            )
        )
        order.total_price += price
    await test_db_session.commit()
