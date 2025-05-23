from fastapi import APIRouter, Depends, Request, Form, Path, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.dependencies import get_user_manager, current_user
from src.core.authentification.user_manager import UserManager
from src.core.cruds.dependencies import get_user_by_id
from src.core.cruds.users import (
    create_user,
    update_user,
    get_users_list,
    delete_user,
)
from src.core.models import db_helper, User
from src.core.schemas.users import UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get("/", name="web/users")
async def users_list(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    users = await get_users_list(session)
    return templates.TemplateResponse(
        "cafe/users_list.html", {"request": request, "users": users}
    )


@router.get("/new/", name="web/user_create")
async def user_create(request: Request):
    return templates.TemplateResponse(
        "cafe/user_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/user_create"),
            "current_email": "",
            "is_edit": False,
        },
    )


@router.post("/new/", name="web/user_create")
async def user_create(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user_create = UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
        user = await create_user(
            user_manager=user_manager,
            user_create=user_create,
        )
        return RedirectResponse(
            url=request.url_for("web/user_detail", pk=user.id), status_code=302
        )
    except ValueError as e:
        error_msg = str(e)
    except Exception as e:
        error_msg = f"Ошибка при создании пользователя: {str(e)}"

    return templates.TemplateResponse(
        "cafe/user_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/user_create"),
            "current_email": email,
            "error": error_msg,
            "is_edit": False,
        },
        status_code=400,
    )


@router.get("/{pk}/", name="web/user_detail")
async def user_details(
    request: Request,
    user: User = Depends(get_user_by_id),
    current_user: User = Depends(current_user),
):
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return templates.TemplateResponse(
        "cafe/user_detail.html", {"request": request, "user": user}
    )


@router.get("/{pk}/edit/", name="web/user_update")
async def user_update(
    request: Request,
    user: User = Depends(get_user_by_id),
):
    return templates.TemplateResponse(
        "cafe/user_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/user_update", pk=user.id),
            "current_email": user.email,
            "is_edit": True,
            "user": user,
        },
    )


@router.post("/{pk}/edit/", name="web/user_update")
async def user_update(
    request: Request,
    pk: int = Path(...),
    email: str = Form(...),
    password: str = Form(default=None),
    user_manager: UserManager = Depends(get_user_manager),
):
    user = await get_user_by_id(pk=pk, user_manager=user_manager)
    try:
        update_data = UserUpdate(email=email)
        if password:
            update_data.password = password
        await update_user(
            user=user,
            user_manager=user_manager,
            user_update=update_data,
        )
        return RedirectResponse(
            url=request.url_for("web/user_detail", pk=user.id), status_code=302
        )
    except Exception as e:
        print(f"user_update Exception: {e}, Exception.args: {e.args}")
        return templates.TemplateResponse(
            "cafe/user_form.html",
            {
                "request": request,
                "action_url": request.url_for("web/user_update", pk=user.id),
                "current_email": email,
                "error": str(e),
                "is_edit": True,
                "user": user,
            },
            status_code=400,
        )


@router.post("/{pk}/delete/", name="web/user_delete")
async def user_delete(
    request: Request,
    pk: int = Path(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    user = await get_user_by_id(pk=pk, user_manager=user_manager)
    await delete_user(user_manager=user_manager, user=user, request=request)
    return RedirectResponse(url=request.url_for("web/users"), status_code=302)
