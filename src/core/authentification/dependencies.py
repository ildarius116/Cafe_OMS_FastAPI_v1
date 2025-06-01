from contextlib import asynccontextmanager
from fastapi import Depends, Request, HTTPException, status
from fastapi_users.authentication import Authenticator
from fastapi_users.authentication.strategy import DatabaseStrategy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List


from src.api.dependencies.authentification import (
    get_access_tokens_db,
    authentication_backend,
    get_database_strategy,
    get_users_db,
    get_user_manager,
)
from src.core.authentification.user_manager import UserManager
from src.core.config import settings
from src.core.cruds.dependencies import get_user_by_id
from src.core.models import db_helper, User, Role

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
) -> User | None:
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
                auth_user = await strategy.read_token(token, user_manager)
                user = await get_user_by_id(session=session, pk=auth_user.id)
                return user
    except Exception:
        return None


async def get_current_user_permissions(
    current_user: User = Depends(current_user_optional),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[str]:
    if not current_user:
        return []

    result = await session.execute(
        select(User)
        .where(User.id == current_user.id)
        .options(selectinload(User.roles).selectinload(Role.permissions))
    )
    user = result.scalar_one()

    return [perm.name for role in user.roles for perm in role.permissions]


def permission_required(permission: str):
    async def checker(
        current_user: User = Depends(current_user_optional),
        permissions: List[str] = Depends(get_current_user_permissions),
    ):
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )
        return current_user

    return Depends(checker)
