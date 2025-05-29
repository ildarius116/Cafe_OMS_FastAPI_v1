import asyncio
import contextlib

from src.api.dependencies.authentification.users import get_users_db
from src.api.dependencies.authentification.user_manager import get_user_manager
from src.core.authentification.user_manager import UserManager
from src.core.models import db_helper, User
from src.core.schemas.users import UserCreate


get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

emails_list = [
    "user1@test.com",
    "user2@test.com",
    "user3@test.com",
    "user4@test.com",
]
passwords_list = [
    "user1111",
    "user2222",
    "user3333",
    "user4444",
]
active_status_list = [
    True,
    True,
    True,
    False,
]
verified_status_list = [
    True,
    True,
    False,
    True,
]
default_is_superuser = False


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_testuser(
    email: str,
    password: str,
    is_active: bool,
    is_verified: bool,
    is_superuser: bool = default_is_superuser,
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


if __name__ == "__main__":
    for i in range(len(emails_list)):
        asyncio.run(
            create_testuser(
                email=emails_list[i],
                password=passwords_list[i],
                is_active=active_status_list[i],
                is_verified=verified_status_list[i],
            )
        )
