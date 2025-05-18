from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from src.core.models import db_helper, AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.get_scoped_session),
    ],
):
    yield AccessToken.get_db(session=session)
