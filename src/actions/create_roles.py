import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.models import db_helper, Role
from src.core.schemas.roles import RoleCreate

log = logging.getLogger(__name__)


def role_data() -> list:
    """Функция списка данных для создания заказов"""
    data_list: List[RoleCreate] = [
        RoleCreate(name="guest"),
        RoleCreate(name="stuff"),
        RoleCreate(name="manager"),
        RoleCreate(name="admin"),
        RoleCreate(name="superuser"),
    ]
    return data_list


async def create_roles(
    role_data: List[RoleCreate],
    session: AsyncSession,
) -> None:
    """Функция создания заказов"""
    for role_in in role_data:
        role: Role = Role(**role_in.model_dump())
        session.add(role)
    await session.commit()
    log.warning(f"Created {len(role_data)} roles")


if __name__ == "__main__":
    role_data = role_data()
    session = db_helper.get_scoped_session()
    asyncio.run(create_roles(role_data=role_data, session=session))
