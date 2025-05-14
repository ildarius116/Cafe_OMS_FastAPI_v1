from fastapi import APIRouter, status, Depends
from typing import List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.menu_items.crud import (
    create_menu_item,
    get_menu_items_list,
    update_menu_item,
    delete_menu_item,
)
from src.core.schemas.menu_items import (
    MenuItemSchema,
    MenuItemCreateSchema,
    MenuItemUpdateSchema,
    MenuItemUpdatePartialSchema,
)
from src.core.models import db_helper, MenuItemModel
from src.api_v1.menu_items.dependencies import get_menu_item_by_id


load_dotenv()
router = APIRouter()


@router.get(
    path="/",
    response_model=List[MenuItemSchema],
    summary="Вывести список элементов Меню",
)
async def menu_items_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    return await get_menu_items_list(session=session)


@router.post(
    path="/",
    response_model=MenuItemSchema,
    summary="Создать элемент Меню",
    status_code=status.HTTP_201_CREATED,
)
async def menu_item_create(
    menu_item_in: MenuItemCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await create_menu_item(session=session, menu_item_in=menu_item_in)


@router.get(
    path="/{pk}/",
    response_model=MenuItemSchema,
    summary="Вывести определенный элемент Меню",
)
async def menu_item_one(
    menu_item: MenuItemModel = Depends(get_menu_item_by_id),
):
    """
    pk - id элемента Меню.
    """
    return menu_item


@router.put(
    path="/{pk}/",
    response_model=MenuItemSchema,
    summary="Полное обновление элемента Меню",
)
async def menu_item_update_full(
    item_update: MenuItemUpdateSchema,
    menu_item: MenuItemModel = Depends(get_menu_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await update_menu_item(
        session=session,
        menu_item=menu_item,
        item_update=item_update,
    )


@router.patch(
    path="/{pk}/",
    response_model=MenuItemSchema,
    summary="Частичное обновление элемента Меню",
)
async def menu_item_update_partial(
    item_update: MenuItemUpdatePartialSchema,
    menu_item: MenuItemModel = Depends(get_menu_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    pk - id элемента Меню.
    name - название элемента Меню.
    price - стоимость элемента Меню.
    """
    return await update_menu_item(
        session=session,
        menu_item=menu_item,
        item_update=item_update,
        partial=True,
    )


@router.delete(
    path="/{pk}/",
    summary="Удаление элемента Меню",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def menu_item_delete(
    menu_item: MenuItemModel = Depends(get_menu_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    pk - id элемента Меню.
    """
    await delete_menu_item(session=session, menu_item=menu_item)
