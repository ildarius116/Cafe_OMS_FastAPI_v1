from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from src.api.dependencies.authentification.access_tokens import get_access_tokens_db
from src.core.models import db_helper
from src.core.config import settings

if TYPE_CHECKING:
    from src.core.models import AccessToken
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_database_strategy(
    session: Annotated["AsyncSession", Depends(db_helper.session_dependency)],
) -> DatabaseStrategy:
    async with get_access_tokens_db(session) as access_tokens_db:
        return DatabaseStrategy(
            database=access_tokens_db,
            lifetime_seconds=settings.access_token.lifetime_seconds,
        )
