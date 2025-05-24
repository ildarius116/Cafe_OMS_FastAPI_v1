import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.models import db_helper, Permission, Role, User
from src.core.schemas.permissions import PermissionCreate

log = logging.getLogger(__name__)


def permissions_data() -> list:
    """Функция списка данных для создания заказов"""
    data_list: List[PermissionCreate] = [
        PermissionCreate(name="read_permission"),
        PermissionCreate(name="read_all_permissions"),
        PermissionCreate(name="create_permission"),
        PermissionCreate(name="update_permission"),
        PermissionCreate(name="delete_permission"),
        PermissionCreate(name="add_permission_to_role"),
        PermissionCreate(name="remove_permission_from_role"),
        PermissionCreate(name="read_role"),
        PermissionCreate(name="read_all_roles"),
        PermissionCreate(name="create_role"),
        PermissionCreate(name="update_role"),
        PermissionCreate(name="delete_role"),
        PermissionCreate(name="add_role_to_user"),
        PermissionCreate(name="remove_role_from_user"),
        PermissionCreate(name="read_user"),
        PermissionCreate(name="read_all_users"),
        PermissionCreate(name="create_user"),
        PermissionCreate(name="update_user"),
        PermissionCreate(name="delete_user"),
    ]
    return data_list


async def create_permissions(
    permissions_data: List[PermissionCreate],
    session: AsyncSession,
) -> None:
    """Функция создания заказов"""
    for permission_in in permissions_data:
        permission: Permission = Permission(**permission_in.model_dump())
        session.add(permission)
    await session.commit()
    log.warning(f"Created {len(permissions_data)} permissions")


if __name__ == "__main__":
    permissions_data = permissions_data()
    session = db_helper.get_scoped_session()
    asyncio.run(create_permissions(permissions_data=permissions_data, session=session))
