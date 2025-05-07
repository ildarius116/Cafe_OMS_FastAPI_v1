from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.pool import NullPool

from src.core.config import settings


class DatabaseHelper:

    def __init__(self, url: str, echo: bool = False):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            poolclass=NullPool,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.debug,
)
