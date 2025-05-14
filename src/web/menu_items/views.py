from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any, List, Annotated
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.menu_items.crud import get_menu_items_list
from src.core.config import settings
from src.core.models import db_helper

load_dotenv()

router = APIRouter()

pk_type = Annotated[int, Path(ge=1, lt=1_000_000)]


@router.get(
    path="/",
    name="menu_item_list",
    summary="menu_item",
)
async def menu_item_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    return await get_menu_items_list(session=session)


@router.get(
    path="/list/",
    name="menu_items_list",
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
    name="menu_item_create",
    # response_model=MenuItemSchema,
    summary="menu_item_create",
)
async def menu_item_create(item) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "menu_item_create"}
    return message


@router.post(
    path="/new/",
    name="menu_item_create",
    # response_model=MenuItemSchema,
    summary="menu_item_create",
)
async def menu_item_create(request) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "menu_item_create"}
    return message


@router.get(
    path="/{pk}/delete/",
    name="menu_item_delete",
    summary="menu_item_delete",
)
async def menu_item_delete(pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "menu_item_delete", "pk": pk}
    return message
