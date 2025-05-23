from contextlib import asynccontextmanager

from fastapi import Depends, Request
from fastapi_users.authentication import Authenticator
from fastapi_users.authentication.strategy import DatabaseStrategy

from src.api.dependencies.authentification.access_tokens import get_access_tokens_db
from src.api.dependencies.authentification.backend import authentication_backend
from src.api.dependencies.authentification.strategy import get_database_strategy
from src.api.dependencies.authentification.users import get_users_db
from src.api.dependencies.authentification.user_manager import get_user_manager
from src.core.authentification.user_manager import UserManager
from src.core.config import settings
from src.core.models import db_helper

get_users_db_context = asynccontextmanager(get_users_db)
get_user_manager_context = asynccontextmanager(get_user_manager)


async def get_user_manager():
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                yield user_manager


async def get_strategy():
    async with db_helper.session_factory() as session:
        async with get_access_tokens_db(session) as access_tokens_db:
            strategy = get_database_strategy(access_tokens_db)
            return strategy


def get_authenticator():
    return Authenticator(
        backends=[authentication_backend],
        get_user_manager=get_user_manager,
    )


current_user = get_authenticator().current_user()


async def current_user_optional(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
):
    token = request.cookies.get("auth_token")
    if not token:
        return None

    try:
        async with db_helper.session_factory() as session:
            async with get_access_tokens_db(session) as access_tokens_db:
                strategy = DatabaseStrategy(
                    database=access_tokens_db,
                    lifetime_seconds=settings.access_token.lifetime_seconds,
                )
                user = await strategy.read_token(token, user_manager)
                return user
    except Exception:
        return None
