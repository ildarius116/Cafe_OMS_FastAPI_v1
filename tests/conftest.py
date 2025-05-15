import pytest_asyncio
from sqlalchemy import delete, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from src.core.config import settings
from src.core.models import Base, OrderModel, MenuItemModel, OrderMenuAssociation

engine: AsyncEngine = create_async_engine(
    url=settings.db_test_url,
    poolclass=NullPool,
    echo=settings.debug
)

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


@pytest_asyncio.fixture(scope="module")
async def test_db():
    """
    Функция-фикстура инициализации и очистка тестовой БД
    """

    async with engine.begin() as conn:
        print('BEFORE CREATE !!!!!!!!!!!!!!!!!')
        await conn.run_sync(Base.metadata.create_all)
        print('AFTER CREATE !!!!!!!!!!!!!!!!!')
    yield
    async with engine.begin() as conn:
        print('BEFORE DROP !!!!!!!!!!!!!!!!!')
        await conn.run_sync(Base.metadata.drop_all)
        print('AFTER DROP !!!!!!!!!!!!!!!!!')


@pytest_asyncio.fixture
async def test_db_session(test_db) -> AsyncSession:
    """
    Функция-фикстура асинхронной сессии
    """
    async with async_session() as session:
        yield session
        await session.close()


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

