from fastapi import APIRouter, status, Depends
from typing import List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.orders import (
    create_order,
    get_order_list,
    update_order,
    delete_order,
)
from src.core.schemas.orders import (
    OrderSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)
from src.core.models import db_helper, OrderModel
from src.core.dependencies import get_order_by_id

load_dotenv()
router = APIRouter()


@router.get(
    path="/",
    response_model=List[OrderSchema],
    summary="Вывести список заказов",
)
async def order_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """ """
    table_number = None
    status = None
    fltr = {}
    if table_number:
        fltr["table_number"] = table_number
    if status:
        fltr["status"] = status
    orders = await get_order_list(session=session, fltr=fltr)
    return orders


@router.post(
    path="/",
    response_model=OrderSchema,
    summary="Создать заказ",
    status_code=status.HTTP_201_CREATED,
)
async def order_create(
    order_in: OrderCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    table_number - номер стола заказа.
    """
    return await create_order(session=session, order_in=order_in)


@router.get(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Вывести определенный заказ",
)
async def order_one(
    order: OrderModel = Depends(get_order_by_id),
):
    """
    pk - id заказа.
    """
    return order


@router.put(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Полное обновление заказа",
    status_code=201,
)
async def order_update_full(
    order_update: OrderUpdateSchema,
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id заказа.\n
    table_number - номер стола заказа.\n
    status - статус заказа.\n
    table_number - номер стола заказа.\n
    total_price - полная стоимость заказа.\n
    menu_items_details - список элементов меню в заказе.\n
    """
    return await update_order(
        session=session,
        order=order,
        order_update=order_update,
    )


@router.patch(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Частичное обновление заказа",
    status_code=201,
)
async def order_update_partial(
    order_update: OrderUpdatePartialSchema,
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id заказа.\n
    table_number - номер стола заказа.\n
    status - статус заказа.\n
    table_number - номер стола заказа.\n
    total_price - полная стоимость заказа.\n
    menu_items_details - список элементов меню в заказе.\n
    """
    return await update_order(
        session=session,
        order=order,
        order_update=order_update,
        partial=True,
    )


@router.delete(
    path="/{pk}/",
    summary="Удаление заказа",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def order_delete(
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    pk - id заказа.
    """
    await delete_order(session=session, order=order)
