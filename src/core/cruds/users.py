from typing import List
from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.user_manager import UserManager
from src.core.models import User, db_helper
from src.core.schemas.users import UserCreate, UserUpdate


async def create_user(
    user_create: UserCreate,
    user_manager: UserManager,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=True,
    )
    return user


async def get_user_by_email(
    email: str,
    user_manager: UserManager,
) -> User:
    return await user_manager.get_by_email(user_email=email)


async def get_users_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return list(users)


async def update_user(
    user: User,
    user_update: UserUpdate,
    user_manager: UserManager,
) -> User:
    upd_user = await user_manager.update(
        user=user,
        user_update=user_update,
        safe=True,
    )
    return upd_user


async def delete_user(
    user: User,
    request: Request,
    user_manager: UserManager,
) -> None:
    await user_manager.delete(user, request=request)
