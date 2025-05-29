from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from sqlalchemy.orm import selectinload

from src.core.models import Role, User
from src.core.schemas.roles import RoleCreate, RoleUpdate


async def create_role(session: AsyncSession, role_in: RoleCreate) -> Role:
    role = Role(name=role_in.name)
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def get_role_by_id(session: AsyncSession, pk: int) -> Role | None:
    return await session.get(Role, pk)


async def get_role_by_name(session: AsyncSession, name: str) -> Role | None:
    query = select(Role).where(Role.name == name)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Role {name} not found!",
    )


async def get_roles_list(session: AsyncSession) -> List[Role]:
    query = (
        select(Role)
        .options(
            selectinload(Role.permissions),
        )
        .order_by(Role.id)
    )
    result = await session.execute(query)
    result = result.scalars().all()
    return list(result)


async def update_role(
    session: AsyncSession,
    role: Role,
    role_update: RoleUpdate,
) -> Role | None:
    if not role:
        return None
    for key, value in role_update.model_dump(exclude_unset=True).items():
        setattr(role, key, value)
    await session.commit()
    await session.refresh(role)
    return role


async def delete_role(session: AsyncSession, role: Role) -> bool:
    if not role:
        return False
    await session.delete(role)
    await session.commit()
    return True


async def add_role_to_user(session: AsyncSession, user: User, role: Role):
    if role not in user.roles:
        user.roles.append(role)
        await session.commit()
        await session.refresh(user)
    return user


async def remove_role_from_user(session: AsyncSession, user: User, role: Role):
    if role in user.roles:
        user.roles.remove(role)
        await session.commit()
        await session.refresh(user)
    return user
