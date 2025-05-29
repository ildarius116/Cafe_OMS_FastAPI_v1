import asyncio
import logging
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.permissions import (
    get_permissions_list,
    add_permission_to_role,
)
from src.core.cruds.roles import get_roles_list
from src.core.models import db_helper, Permission

log = logging.getLogger(__name__)


roles_for_guest = [
    "read_user",
    "read_order",
    "read_all_orders",
]
roles_for_stuff = [
    "read_user",
    "read_order",
    "read_all_orders",
    "create_order",
    "update_order",
    "delete_order",
    "read_menu_item",
    "read_all_menu_items",
    "add_menu_item_into_order",
    "del_menu_item_from_order",
]
roles_for_manager = [
    "read_user",
    "read_order",
    "read_all_orders",
    "create_order",
    "update_order",
    "delete_order",
    "read_menu_item",
    "read_all_menu_items",
    "create_menu_item",
    "update_menu_item",
    "delete_menu_item",
    "add_menu_item_into_order",
    "del_menu_item_from_order",
]
roles_for_admin = [
    "read_user",
    "read_all_users",
    "create_user",
    "update_user",
    "delete_user",
    "read_role",
    "read_all_roles",
    "add_role_to_user",
    "remove_role_from_user",
    "read_all_orders",
    "read_order",
    "read_all_orders",
    "create_order",
    "update_order",
    "delete_order",
    "read_menu_item",
    "read_all_menu_items",
    "create_menu_item",
    "update_menu_item",
    "delete_menu_item",
    "add_menu_item_into_order",
    "del_menu_item_from_order",
]

perms_to_role_dict = {
    "guest": roles_for_guest,
    "stuff": roles_for_stuff,
    "manager": roles_for_manager,
    "admin": roles_for_admin,
}


async def create_permissions_dict(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    permissions_dict = {}
    permissions = await get_permissions_list(
        session=session,
        skip=0,
        limit=100,
    )
    for permission in permissions:
        permissions_dict[permission.name] = permission
    return permissions_dict


async def create_associations(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """Функция с предсозданными ассоциациями"""
    roles = await get_roles_list(session=session)
    permissions_dict = await create_permissions_dict(session=session)

    for role in roles:
        i = 0
        if role.name != "superuser":
            for i, permission in enumerate(perms_to_role_dict[role.name]):
                await add_permission_to_role(
                    session=session, role=role, permission=permissions_dict[permission]
                )
        else:
            for i, permission in enumerate(permissions_dict.values()):
                await add_permission_to_role(
                    session=session, role=role, permission=permission
                )

        log.warning(f"Added {i+1} permissions for role: {role.name}")
    await session.commit()
    log.warning(f"Modifies {len(roles)} roles")


if __name__ == "__main__":
    session = db_helper.get_scoped_session()
    asyncio.run(create_associations(session=session))
