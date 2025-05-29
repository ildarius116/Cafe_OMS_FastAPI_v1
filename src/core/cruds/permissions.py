from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.models import Permission, Role
from src.core.schemas.permissions import PermissionCreate, PermissionUpdate


async def create_permission(
    session: AsyncSession, permission_in: PermissionCreate
) -> Permission:
    permission = Permission(name=permission_in.name)
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return permission


async def get_permission(session: AsyncSession, pk: int) -> Permission | None:
    return await session.get(Permission, pk)


async def get_permissions_list(
    session: AsyncSession, skip: int, limit: int
) -> List[Permission]:
    query = select(Permission).offset(skip).limit(limit).order_by(Permission.id)
    result = await session.execute(query)
    result = result.scalars().all()
    return list(result)


async def update_permission(
    session: AsyncSession,
    permission: Permission,
    permission_update: PermissionUpdate,
) -> Permission | None:
    if not permission:
        return None
    for key, value in permission_update.dict(exclude_unset=True).items():
        setattr(permission, key, value)
    await session.commit()
    await session.refresh(permission)
    return permission


async def delete_permission(session: AsyncSession, permission: Permission) -> bool:
    if not permission:
        return False
    await session.delete(permission)
    await session.commit()
    return True


async def add_permission_to_role(
    session: AsyncSession, role: Role, permission: Permission
) -> Role:
    if permission not in role.permissions:
        role.permissions.append(permission)
        await session.commit()
        await session.refresh(role)
    return role


async def remove_permission_from_role(
    session: AsyncSession, role: Role, permission: Permission
) -> Role:
    role.permissions.remove(permission)
    await session.commit()
    await session.refresh(role)
    return role
