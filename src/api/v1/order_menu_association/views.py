from fastapi import APIRouter, status, Depends
from typing import List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cruds.order_menu_association import (
    add_menu_item_into_order,
    del_menu_item_from_order,
    get_associations_list,
)
from src.core.schemas.order_menu_association import (
    OrderMenuAssociationSchema,
    OrderMenuAssociationAddSchema,
)
from src.core.schemas.orders import OrderSchema
from src.core.models import db_helper, OrderModel, OrderMenuAssociation
from src.core.dependencies import (
    get_menu_item_by_id,
    get_association_by_id,
    get_order_by_id,
)

load_dotenv()
router = APIRouter()


@router.get(
    path="/",
    response_model=List[OrderMenuAssociationSchema],
    summary="Вывести список связей",
)
async def get_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """ """
    result = await get_associations_list(session=session)
    return result


@router.post(
    path="/{pk}/",
    response_model=OrderSchema,
    summary="Добавить элемент Меню в заказ",
    status_code=status.HTTP_201_CREATED,
)
async def add_into_order(
    order: OrderModel = Depends(get_order_by_id),
    menu_item_in: OrderMenuAssociationAddSchema = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id заказа.\n
    menu_item_id - id элемента Меню.\n
    quantity - количество элементов Меню в заказе.\n
    """
    menu_item = await get_menu_item_by_id(session=session, pk=menu_item_in.menu_item_id)
    result = await add_menu_item_into_order(
        session=session,
        order=order,
        menu_item=menu_item,
        quantity=menu_item_in.quantity,
    )
    return result


@router.delete(
    path="/{pk}/",
    summary="Удаление элемента меню из заказа",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def del_from_order(
    association: OrderMenuAssociation = Depends(get_association_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    pk - id элемента связи.
    """
    await del_menu_item_from_order(session=session, association=association)
