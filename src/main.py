import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from src.core.config import settings
from src.api_v1 import router as router_api_v1
from src.web import router as router_web

from src.core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Функция асинхронного контекстного менеджера с инициализацией БД при старте
    """
    try:
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    except Exception as e:
        logging.error(f"Failed to initialize DB: {e}")
        raise


app = FastAPI(lifespan=lifespan)
app.include_router(router_api_v1, prefix=settings.api_v1_prefix)
app.include_router(router_web, prefix=settings.web_prefix)
