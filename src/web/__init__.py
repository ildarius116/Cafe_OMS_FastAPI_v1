from fastapi import APIRouter

from .auth.views import router as auth_router
from .menu_items.views import router as menu_item_router
from .orders.views import router as orders_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Аутентификация и авторизация"],
)

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

router.include_router(
    users_router,
    prefix="/users",
    tags=["Работа с пользователями"],
)
