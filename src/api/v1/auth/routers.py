from fastapi import APIRouter

from src.api.v1.fastapi_users_router import fastapi_users
from src.api.dependencies.authentification.backend import authentication_backend
from src.core.config import settings
from src.core.schemas.users import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)
# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(
        UserRead,
    ),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
