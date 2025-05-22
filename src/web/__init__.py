from fastapi import APIRouter

from .menu_items.views import router as menu_item_router
from .orders.views import router as orders_router

router = APIRouter()
router.include_router(
    menu_item_router,
    prefix="/menu_items",
    tags=["Работа с элементами Меню"],
)

router.include_router(
    orders_router,
    prefix="/orders",
    tags=["Работа с заказами"],
)
