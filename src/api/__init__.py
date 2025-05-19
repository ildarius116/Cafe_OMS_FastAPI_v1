from fastapi import APIRouter

from src.api.v1 import router as router_api_v1
from src.api.v1.auth import router as router_auth
from src.api.v1.users import router as router_users
from src.core.config import settings

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(router_api_v1)
router.include_router(router_auth)
router.include_router(router_users)
