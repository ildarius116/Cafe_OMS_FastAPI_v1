from fastapi import APIRouter, status, Depends
from typing import Dict, Any, List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.orders.crud import (
    create_order,
    get_order_list,
    update_order,
    delete_order,
)
from src.api_v1.orders.schemas import (
    OrderSchema,
    OrderUpdateSchema,
    OrderUpdatePartialSchema,
    OrdersSchema,
    OrderBaseSchema,
    OrderCreateSchema,
)
from src.core.models import db_helper, OrderModel
from src.api_v1.orders.dependencies import get_order_by_id


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
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    orders = await get_order_list(session=session)
    for order in orders:
        print(f"\n order: {order.id}, order: {order}")

    return await get_order_list(session=session)


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
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    print(f"order_create order_in: {order_in}")
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
    pk - id элемента Меню.
    """
    return order


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
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
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
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
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
    pk - id элемента Меню.
    """
    await delete_order(session=session, order=order)
