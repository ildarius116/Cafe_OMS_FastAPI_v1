from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from src.core.models import db_helper, User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.get_scoped_session),
    ],
):
    yield User.get_db(session=session)
