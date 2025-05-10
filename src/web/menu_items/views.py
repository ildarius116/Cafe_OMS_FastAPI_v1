from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any, List, Annotated
from dotenv import load_dotenv

from src.core.config import settings

load_dotenv()

router = APIRouter(prefix="/menu-items", tags=["Работа с элементами Меню"])

pk_type = Annotated[int, Path(ge=1, lt=1_000_000)]


@router.get(
    path="/",
    summary="menu_item",
)
async def menu_item_list() -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "menu_item"}
    return message


@router.get(
    path="/list/",
    summary="menu_item_list",
)
async def menu_items_list() -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "menu_items_list"}
    return message


@router.get(
    path="/new/",
    # response_model=MenuItemSchema,
    summary="menu_item_create",
)
async def menu_item_create(item: MenuItemSchema) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "menu_item_create"}
    return message


@router.post(
    path="/new/",
    response_model=MenuItemSchema,
    summary="menu_item_create",
)
async def menu_item_create(request: MenuItemSchema) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "menu_item_create"}
    return message


@router.get(
    path="/{pk}/delete/",
    summary="menu_item_delete",
)
async def menu_item_delete(pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "menu_item_delete", "pk": pk}
    return message
