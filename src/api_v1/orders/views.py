from fastapi import APIRouter, status, Depends
from typing import List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.orders.crud import (
    create_order,
    get_order_list,
    update_order,
    delete_order,
    add_menu_item_into_order,
)
from src.api_v1.orders.schemas import (
    OrderSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)
from src.core.models import db_helper, OrderModel
from src.api_v1.orders.dependencies import get_order_by_id
from src.api_v1.menu_items.dependencies import get_menu_item_by_id


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
    orders = await get_order_list(session=session)
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


@router.post(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Добавить элемент Меню в заказ",
)
async def add_menu_item(
    order: OrderModel = Depends(get_order_by_id),
    menu_item_id: int = None,
    quantity: int = 1,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id заказа.\n
    menu_item_id - id элемента Меню.\n
    quantity - количество элементов Меню в заказе.\n
    """
    menu_item = await get_menu_item_by_id(session=session, pk=menu_item_id)
    result = await add_menu_item_into_order(
        session=session,
        order=order,
        menu_item=menu_item,
        quantity=quantity,
    )
    return result


@router.put(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Полное обновление заказа",
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
