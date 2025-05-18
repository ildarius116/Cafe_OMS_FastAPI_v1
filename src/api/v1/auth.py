from fastapi import APIRouter

from src.api.v1.fastapi_users_router import fastapi_users
from src.api.dependencies.authentification.backend import authentication_backend
from src.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
)
