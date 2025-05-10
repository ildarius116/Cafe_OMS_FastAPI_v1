from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper, OrderMenuAssociation


async def get_association_by_id(
    pk: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> OrderMenuAssociation:
    """
    Функция получения элемента меню по id..
    """
    query = select(OrderMenuAssociation).where(OrderMenuAssociation.id == pk)
    result = await session.scalar(query)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Association {pk} not found!",
    )
