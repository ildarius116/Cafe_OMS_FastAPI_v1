from fastapi import APIRouter

from .fastapi_users_router import fastapi_users
from src.core.config import settings
from src.core.schemas.users import UserRead, UserUpdate

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
