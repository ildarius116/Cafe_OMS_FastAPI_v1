from fastapi import APIRouter, HTTPException, Path, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_menu_item_by_id, get_order_by_id
from src.core.config import settings
from src.core.cruds.menu_items import get_menu_items_list
from src.core.models import db_helper, OrderModel
from src.core.cruds.order_menu_association import add_menu_item_into_order
from src.core.cruds.orders import (
    get_order_list,
    create_order,
    update_order,
    delete_order,
)
from src.core.schemas.orders import (
    OrderUpdatePartialSchema,
    OrderCreateSchema,
)

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")
pk_type = Annotated[int, Path(ge=1, lt=1_000_000)]


@router.get(
    path="/",
    name="index",
    summary="Вывести список заказов",
)
async def index(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция получения списка заказов.

    :возврат: html-страница списка заказов.
    """

    table_number = request.query_params.get("table")
    status = request.query_params.get("status")
    fltr = {}
    # message = {
    #     "message": "index",
    #     "table_number": table_number,
    #     "status": status,
    # }
    # print("MESSAGE:", message)
    if table_number:
        fltr["table_number"] = table_number
    if status:
        fltr["status"] = status
    orders = await get_order_list(session=session, fltr=fltr)
    return templates.TemplateResponse(
        name="cafe/index.html",
        request=request,
        context={
            "orders": orders,
            "current_table": table_number,
            "current_status": status,
            "status_labels": settings.ORDER_STATUSES,
        },
    )


@router.get(
    path="/new/",
    name="web/order_create",
    summary="order_create",
)
async def order_create(
    request: Request,
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    return templates.TemplateResponse(
        name="cafe/order_form.html",
        request=request,
        context={
            "status": settings.ORDER_STATUSES,
            "current_status": None,
            "current_table": None,
        },
    )


@router.post(
    path="/new/",
    name="web/order_create",
    summary="order_create",
)
async def order_create(
    request: Request,
    table_number: int = Form(...),
    status: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    order_in = OrderCreateSchema(table_number=table_number, status=status)
    if table_number and status:
        order = await create_order(session=session, order_in=order_in)
        return RedirectResponse(url=f"/{order.id}/", status_code=301)
    return templates.TemplateResponse(
        name="cafe/order_form.html",
        request=request,
        context={
            "table_number": None,
            "status": None,
        },
    )


@router.get(
    path="/revenue/",
    name="web/revenue",
    summary="revenue_report",
)
async def revenue_report(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    paid_orders = await get_order_list(session=session, fltr={"status": "paid"})
    total_revenue: float = sum(order.total_price for order in paid_orders)
    return templates.TemplateResponse(
        name="cafe/revenue_report.html",
        request=request,
        context={
            "paid_orders": paid_orders,
            "total_revenue": total_revenue,
            "time_format": settings.time_format_revenue,
        },
    )


@router.post(
    path="/items/{pk}/add/",
    name="web/order_item_add",
    summary="order_item_add",
)
async def order_item_add(
    request: Request,
    menu_item: int = Form(...),
    quantity: int = Form(...),
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    menu_items = await get_menu_items_list(session=session)
    menu_item = await get_menu_item_by_id(session=session, pk=menu_item)
    order = await add_menu_item_into_order(
        session=session,
        order=order,
        menu_item=menu_item,
        quantity=quantity,
    )
    return templates.TemplateResponse(
        name="cafe/order_detail.html",
        request=request,
        context={
            "order": order,
            "menu_items": menu_items,
        },
    )


@router.post(
    path="/items/{pk}/delete/",
    name="web/order_item_delete",
    summary="order_item_delete",
)
async def order_item_delete(
    request,
    pk: pk_type,
) -> Dict[str, Any]:
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    message = {"message": "order_item_delete", "pk": pk}
    return message


@router.get(
    path="/{pk}/",
    name="web/order_details",
    summary="order_detail",
)
async def order_detail(
    request: Request,
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    menu_items = await get_menu_items_list(session=session)
    return templates.TemplateResponse(
        name="cafe/order_detail.html",
        request=request,
        context={
            "order": order,
            "menu_items": menu_items,
        },
    )


@router.get(
    path="/{pk}/edit/",
    name="web/order_update",
    summary="order_update",
)
async def order_update(
    request: Request,
    order: OrderModel = Depends(get_order_by_id),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    return templates.TemplateResponse(
        name="cafe/order_form.html",
        request=request,
        context={
            "order": order,
            "form": order,
            "status": settings.ORDER_STATUSES,
            "current_status": order.status,
            "current_table": order.table_number,
        },
    )


status_labels: Dict[str, str] = {
    "table_number": "Номер стола",
    "status": "Статус заказа",
}


@router.post(
    path="/{pk}/edit/",
    name="web/order_update",
    summary="order_update",
)
async def order_update(
    request: Request,
    table_number: int = Form(...),
    status: str = Form(...),
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    if status not in settings.ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    order_update = OrderUpdatePartialSchema(
        table_number=table_number,
        status=status,
    )
    order = await update_order(
        session=session,
        order=order,
        order_update=order_update,
        partial=True,
    )
    return templates.TemplateResponse(
        name="cafe/order_detail.html",
        request=request,
        context={
            "order": order,
            "table_number": table_number,
            "status": status,
        },
    )


@router.post(
    path="/{pk}/delete/",
    name="web/order_delete",
    summary="order_delete",
)
async def order_delete(
    order: OrderModel = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Функция создания заказа.

    :возврат: html-страница списка заказов.
    """
    await delete_order(session=session, order=order)
    return RedirectResponse(url="/", status_code=302)
