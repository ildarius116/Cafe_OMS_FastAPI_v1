from fastapi import APIRouter, status, Depends
from typing import Dict, Any, List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.order_items.crud import (
    create_order_item,
    get_order_item_list,
    update_order_item,
    delete_order_item,
)
from src.api_v1.order_items.schemas import (
    OrderItemSchema,
    OrderItemUpdateSchema,
    OrderItemUpdatePartialSchema,
    OrderItemCreateSchema,
)
from src.core.models import db_helper, OrderItemModel
from src.api_v1.order_items.dependencies import get_order_item_by_id


load_dotenv()
router = APIRouter()


@router.get(
    path="/",
    response_model=List[OrderItemSchema],
    summary="Вывести список элементов заказов",
)
async def order_item_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    return await get_order_item_list(session=session)


@router.post(
    path="/",
    response_model=OrderItemSchema,
    summary="Создать элемент заказа",
    status_code=status.HTTP_201_CREATED,
)
async def order_item_create(
    order_item_in: OrderItemCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await create_order_item(session=session, order_item_in=order_item_in)


@router.get(
    path="/{pk}/",
    response_model=OrderItemSchema,
    summary="Вывести определенный элемент заказа",
)
async def order_item_one(
    order_item: OrderItemModel = Depends(get_order_item_by_id),
):
    """
    pk - id элемента Меню.
    """
    return order_item


@router.put(
    path="/{pk}/",
    response_model=OrderItemSchema,
    summary="Полное обновление элемента заказа",
)
async def order_item_update_full(
    order_item_update: OrderItemUpdateSchema,
    order_item: OrderItemModel = Depends(get_order_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await update_order_item(
        session=session,
        order_item=order_item,
        order_item_update=order_item_update,
    )


@router.patch(
    path="/{pk}/",
    response_model=OrderItemSchema,
    summary="Частичное обновление элемента заказа",
)
async def order_item_update_partial(
    order_item_update: OrderItemUpdatePartialSchema,
    order_item: OrderItemModel = Depends(get_order_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await update_order_item(
        session=session,
        order_item=order_item,
        order_item_update=order_item_update,
        partial=True,
    )


@router.delete(
    path="/{pk}/",
    summary="Удаление элемента заказа",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def order_item_delete(
    order_item: OrderItemModel = Depends(get_order_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    pk - id элемента Меню.
    """
    await delete_order_item(session=session, order_item=order_item)
