from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.user_manager import UserManager
from src.core.models import User, db_helper
from src.core.schemas.users import UserCreate, UserUpdate


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=True,
    )
    return user


# async def _create_user(
#     session: AsyncSession,
#     user_in: UserCreate,
# ) -> User:
#     user = User(**user_in.model_dump())
#     session.add(user)
#     await session.commit()
#     # user = await session.scalar(select(User).where(User.id == user.id))
#     await session.refresh(user)
#     return user


async def get_user(
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
    user_manager: UserManager,
    user_update: UserUpdate,
) -> User:
    upd_user = await user_manager.update(
        user=user,
        user_update=user_update,
        safe=True,
    )
    return upd_user


# async def update_user(
#     session: AsyncSession,
#     user: User,
#     update_data: UserUpdate,
#     partial: bool = False,
# ) -> User:
#     for key, value in update_data.model_dump(exclude_unset=partial).items():
#         setattr(user, key, value)
#     await session.commit()
#     await session.refresh(user)
#     return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
