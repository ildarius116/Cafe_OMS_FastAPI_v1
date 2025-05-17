from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.cruds.menu_items import (
    get_menu_items_list,
    create_menu_item,
    delete_menu_item,
)
from src.core.dependencies import get_menu_item_by_id
from src.core.models import db_helper, MenuItemModel
from src.core.schemas.menu_items import MenuItemCreateSchema

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get(
    path="/",
    name="web/menu_details",
    summary="menu_details",
)
async def menu_details(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция получения списка заказов.

    :возврат: html-страница списка заказов.
    """

    name = request.query_params.get("name")
    type = request.query_params.get("type")
    fltr = {}
    if name and name != "None":
        fltr["name"] = name
    if type:
        fltr["type"] = type

    menu_items = await get_menu_items_list(session=session, fltr=fltr)
    return templates.TemplateResponse(
        name="cafe/menu_detail.html",
        request=request,
        context={
            "current_name": name,
            "current_type": type,
            "menu_items": menu_items,
            "type_labels": settings.MENU_ITEM_TYPES,
        },
    )


@router.post(
    path="/",
    name="web/menu_item_create",
    summary="menu_item_create",
)
async def menu_item_create(
    name: str = Form(...),
    type: str = Form(...),
    price: float = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    if name and price and type:
        menu_item_in = MenuItemCreateSchema(name=name, type=type, price=price)
        await create_menu_item(session=session, menu_item_in=menu_item_in)
    return RedirectResponse(url="/menu_items/", status_code=status.HTTP_303_SEE_OTHER)


@router.post(
    path="/{pk}/delete/",
    name="web/menu_item_delete",
    summary="menu_item_delete",
)
async def menu_item_delete(
    menu_item: MenuItemModel = Depends(get_menu_item_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """

    await delete_menu_item(session=session, menu_item=menu_item)
    return RedirectResponse(url="/menu_items/", status_code=status.HTTP_303_SEE_OTHER)
