from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.api.dependencies.authentification.backend import authentication_backend
from src.api.dependencies.authentification.strategy import get_database_strategy
from src.core.authentification.dependencies import get_user_manager
from src.core.authentification.user_manager import UserManager
from src.core.models import db_helper

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get("/login/", name="web/login")
async def login_form(request: Request):
    return templates.TemplateResponse(
        "cafe/login_form.html",
        {"request": request, "action_url": request.url_for("web/login")},
    )


@router.post("/login/", name="web/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        async with db_helper.session_factory() as session:
            strategy = await get_database_strategy(session)

            user = await user_manager.get_by_email(email)
            if not user or not await user_manager.validate_password(password, user):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверные учетные данные",
                )

            auth_response = await authentication_backend.login(strategy, user)

            redirect_response = RedirectResponse(
                url=request.url_for("web/user_detail", pk=user.id),
                status_code=status.HTTP_302_FOUND,
            )

            for key, value in auth_response.headers.items():
                if key.lower() == "set-cookie":
                    redirect_response.headers.append(key, value)

            return redirect_response

    except HTTPException as e:
        print(f"[DEBUG] HTTPException: {e.detail}")
        return templates.TemplateResponse(
            "cafe/login_form.html",
            {
                "request": request,
                "error": f"Ошибка входа: {e.detail}",
                "current_email": email,
            },
            status_code=401,
        )
    except Exception as e:
        print(
            f"[DEBUG] Unexpected error: {type(e)} - {type(e).__name__} - {str(e.args)}"
        )
        return templates.TemplateResponse(
            "cafe/login_form.html",
            {
                "request": request,
                "error": f"Ошибка сервера при входе: {type(e).__name__} - {str(e)}",
                "current_email": email,
            },
            status_code=500,
        )


@router.post("/logout/", name="web/logout")
async def logout(
    request: Request,
):
    try:
        token = request.cookies.get("auth_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No authentication token found",
            )

        async with db_helper.session_factory() as session:
            strategy = await get_database_strategy(session)
            response = RedirectResponse(
                url=request.url_for("web/login"), status_code=302
            )
            await authentication_backend.logout(strategy, response, token)
            return response

    except HTTPException as e:
        response = RedirectResponse(url=request.url_for("web/login"), status_code=302)
        response.delete_cookie("auth_token")
        return response
    except Exception as e:
        print(f"[DEBUG] Error during logout: {e}")
        response = RedirectResponse(url=request.url_for("web/login"), status_code=302)
        response.delete_cookie("auth_token")
        return response
