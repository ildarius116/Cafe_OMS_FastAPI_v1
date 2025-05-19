from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.api.v1 import router as router_api_v1
from src.api.v1.auth.routers import router as router_auth
from src.api.v1.users.routers import router as router_users
from src.core.config import settings

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(router_api_v1)
router.include_router(router_auth)
router.include_router(router_users)
