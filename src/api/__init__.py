from fastapi import APIRouter

from src.api.v1 import router as router_api_v1
from src.api.v1.auth import router as router_auth

router = APIRouter()
router.include_router(router_api_v1)
router.include_router(router_auth)
