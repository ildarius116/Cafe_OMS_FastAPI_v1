import logging
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.models import Base, db_helper
from src.api import router as router_api_v1
from src.web import router as router_web

templates = Jinja2Templates(directory="src/web/templates")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Функция асинхронного контекстного менеджера с инициализацией БД при старте
    """
    try:
        yield
    except Exception as e:
        logging.error(f"Failed to initialize DB: {e}")
        raise


app = FastAPI(lifespan=lifespan)
app.include_router(router_api_v1, prefix=settings.api.prefix)
app.include_router(router_web, prefix=settings.web.prefix)


@app.get(
    path="/",
    name="index",
    summary="Стартовая страница",
)
async def index(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция получения списка заказов.

    :возврат: html-страница списка заказов.
    """
    user = request.query_params.get("user")
    return templates.TemplateResponse(
        name="cafe/index.html",
        request=request,
        context={
            "current_user": user,
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
