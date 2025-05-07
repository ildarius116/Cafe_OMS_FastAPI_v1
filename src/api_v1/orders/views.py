from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any, List, Annotated
from dotenv import load_dotenv

from src.core.config import settings

load_dotenv()

router = APIRouter()

pk_type = Annotated[int, Path(ge=1, lt=1_000_000)]


@router.get(
    path="/",
    summary="Orders list",
)
async def order_list() -> Dict[str, Any]:
    """
    Функция получения списка заказов.

    :возврат: html-страница списка заказов.
    """
    return {"massage": "order list"}


@router.get(
    path="/new/",
    summary="order_create",
)
async def order_create() -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    return {"message": "new order"}


@router.post(
    path="/new/",
    summary="order_create",
)
async def order_create(request) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "new order"}
    return message


@router.get(
    path="/revenue/",
    # response_model=AddressResponseSchema,
    summary="revenue_report",
)
async def revenue_report() -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "revenue_report"}
    return message


@router.post(
    path="/items/{pk}/add/",
    summary="order_item_add",
)
async def order_item_add(request, pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "order_item_add", "pk": pk}
    return message


@router.post(
    path="/items/{pk}/delete/",
    # response_model=AddressResponseSchema,
    summary="order_item_delete",
)
async def order_item_delete(request, pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "order_item_delete", "pk": pk}
    return message


@router.get(
    path="/{pk}/",
    # response_model=AddressResponseSchema,
    summary="order_detail",
)
async def order_detail(pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "order_detail", "pk": pk}
    return message


@router.get(
    path="/{pk}/edit/",
    # response_model=AddressResponseSchema,
    summary="order_update",
)
async def order_update(pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "order_update", "pk": pk}
    return message


@router.get(
    path="/{pk}/edit/",
    # response_model=AddressResponseSchema,
    summary="order_update",
)
async def order_update(request, pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "order_update", "pk": pk}
    return message


@router.get(
    path="/{pk}/delete/",
    # response_model=AddressResponseSchema,
    summary="order_delete",
)
async def order_delete(pk: pk_type) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    message = {"message": "order_delete", "pk": pk}
    return message
