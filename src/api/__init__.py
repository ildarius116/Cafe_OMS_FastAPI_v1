from fastapi import APIRouter

from src.api.v1 import router as router_api_v1

router = APIRouter()
router.include_router(router_api_v1)
