import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from typing import AsyncGenerator, Any, Optional

from src.core.authentification.dependencies import current_user_optional
from src.core.config import settings
from src.core.models import User

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
    current_user: Optional[User] = Depends(current_user_optional),
):
    """
    Функция стартовой страницы.

    :возврат: html-страница приветствия.
    """
    print(f"index current_user: {current_user}")
    return templates.TemplateResponse(
        name="cafe/index.html",
        request=request,
        context={
            "current_user": current_user,
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
