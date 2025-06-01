import asyncio
import logging
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.roles import get_roles_list, add_role_to_user
from src.core.cruds.users import get_users_list
from src.core.models import db_helper

log = logging.getLogger(__name__)


user_to_role_dict = {
    "user1@test.com": "guest",
    "user2@test.com": "stuff",
    "user3@test.com": "manager",
    "user4@test.com": "admin",
    "admin@admin.com": "superuser",
}


async def create_roles_dict(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    roles_dict = {}
    roles = await get_roles_list(session=session)
    for role in roles:
        roles_dict[role.name] = role
    return roles_dict


async def create_associations(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """Функция с предсозданными ассоциациями"""
    users = await get_users_list(session=session)

    roles_dict = await create_roles_dict(session=session)

    for user in users:
        if user.email == "admin@admin.com":
            role = user_to_role_dict[user.email]
            await add_role_to_user(session=session, user=user, role=roles_dict[role])
        else:
            role = user_to_role_dict[user.email]
            await add_role_to_user(session=session, user=user, role=roles_dict[role])

        log.warning(f"Added role: {role} for user: {user.email}")
    await session.commit()
    log.warning(f"Modifies {len(users)} users")


if __name__ == "__main__":
    session = db_helper.get_scoped_session()
    asyncio.run(create_associations(session=session))
