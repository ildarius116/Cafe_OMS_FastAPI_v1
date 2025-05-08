from fastapi import APIRouter

from .menu_items.views import router as menu_item_router_api
from .order_items.views import router as order_item_router_api
from .orders.views import router as orders_router_api

router = APIRouter()
router.include_router(
    menu_item_router_api, prefix="/menu_items", tags=["API Работа с элементами Меню"]
)
router.include_router(
    order_item_router_api,
    prefix="/order_items",
    tags=["API Работа с элементами заказа"],
)
router.include_router(
    orders_router_api, prefix="/orders", tags=["API Работа с заказами"]
)
