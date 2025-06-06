from fastapi import APIRouter, Depends, Request, Form, Path, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.authentification.dependencies import (
    get_user_manager,
    permission_required,
    current_user_optional,
)
from src.core.authentification.user_manager import UserManager
from src.core.cruds.dependencies import get_user_by_id_dep
from src.core.cruds.roles import (
    add_role_to_user,
    get_role_by_name,
    remove_role_from_user,
)
from src.core.models import db_helper, User, Role
from src.core.cruds.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users_list,
    update_user,
)
from src.core.schemas.users import UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get(
    "/",
    name="web/users",
    dependencies=[permission_required("read_all_users")],
)
async def users_list(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    users = await get_users_list(session)
    return templates.TemplateResponse(
        "cafe/users_list.html", {"request": request, "users": users}
    )


@router.get(
    "/new/",
    name="web/user_create",
    dependencies=[permission_required("create_user")],
)
async def user_create(request: Request):
    return templates.TemplateResponse(
        "cafe/user_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/user_create"),
            "current_email": "",
            "role": Role.DEFAULT_USER_ROLES,
            "current_role": None,
            "is_edit": False,
        },
    )


@router.post(
    "/new/",
    name="web/user_create",
    dependencies=[permission_required("create_user")],
)
async def user_create(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(db_helper.session_dependency),
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
        print(f"user_create created user: {user}")
        user = await get_user_by_id_dep(session=session, pk=user.id)
        print(f"user_create got user: {user}")
        if role:
            role = await get_role_by_name(session=session, name=role)
        else:
            role = await get_role_by_name(session=session, name="guest")
        print(f"user_create guest_role: {role}")
        user = await add_role_to_user(session=session, user=user, role=role)
        print(f"user_create guest user: {user}")
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
            "current_role": None,
            "error": error_msg,
            "is_edit": False,
        },
        status_code=400,
    )


@router.get(
    "/{pk}/",
    name="web/user_detail",
    dependencies=[permission_required("read_user")],
)
async def user_details(
    request: Request,
    user: User = Depends(get_user_by_id_dep),
    current_user: User = Depends(current_user_optional),
):

    if user.id != current_user.id and not any(
        (role.name == "admin" or role.name == "superuser")
        for role in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    return templates.TemplateResponse(
        "cafe/user_detail.html", {"request": request, "user": user}
    )


@router.get(
    "/{pk}/edit/",
    name="web/user_update",
    dependencies=[permission_required("update_user")],
)
async def user_update(
    request: Request,
    user: User = Depends(get_user_by_id_dep),
    current_user: User = Depends(current_user_optional),
):
    if user.id != current_user.id and not any(
        (role.name == "admin" or role.name == "superuser")
        for role in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    return templates.TemplateResponse(
        "cafe/user_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/user_update", pk=user.id),
            "current_email": user.email,
            "role": Role.DEFAULT_USER_ROLES,
            "current_role": user.roles[0],
            "is_edit": True,
            "user": user,
        },
    )


@router.post(
    "/{pk}/edit/",
    name="web/user_update",
    dependencies=[permission_required("update_user")],
)
async def user_update(
    request: Request,
    pk: int = Path(...),
    email: str = Form(...),
    password: str = Form(default=None),
    role: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
    current_user: User = Depends(current_user_optional),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await get_user_by_id(id=pk, user_manager=user_manager)

    if user.id != current_user.id and not any(
        (role.name == "admin" or role.name == "superuser")
        for role in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    try:
        update_data = UserUpdate(email=email)
        if password:
            update_data.password = password

        await update_user(
            user=user,
            user_manager=user_manager,
            user_update=update_data,
        )
        if role:
            user = await get_user_by_id_dep(session=session, pk=user.id)
            if role != user.roles[0]:
                role_to_delete = await get_role_by_name(
                    session=session, name=user.roles[0].name
                )
                user = await remove_role_from_user(
                    session=session, user=user, role=role_to_delete
                )
                role = await get_role_by_name(session=session, name=role)
                user = await add_role_to_user(session=session, user=user, role=role)
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
                "current_role": user.roles[0],
                "error": str(e),
                "is_edit": True,
                "user": user,
            },
            status_code=400,
        )


@router.post(
    "/{pk}/delete/",
    name="web/user_delete",
    dependencies=[permission_required("delete_user")],
)
async def user_delete(
    request: Request,
    pk: int = Path(...),
    user_manager: UserManager = Depends(get_user_manager),
    current_user: User = Depends(current_user_optional),
):
    user = await get_user_by_id(id=pk, user_manager=user_manager)

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Нельзя удалить свой собственный аккаунт"
        )

    if not any(
        (role.name == "admin" or role.name == "superuser")
        for role in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    await delete_user(user_manager=user_manager, user=user, request=request)
    return RedirectResponse(url=request.url_for("web/users"), status_code=302)
