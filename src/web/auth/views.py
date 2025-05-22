from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.core.authentification.user_manager import UserManager
from src.core.dependencies import get_user_manager

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")


@router.get("/login/", name="web/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "cafe/login_form.html",
        {
            "request": request,
            "action_url": request.url_for("web/login"),
            "current_email": "",
        },
    )


@router.post("/login/", name="web/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        try:
            user = await user_manager.get_by_email(email)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль!",
            )

        is_valid = await user_manager.validate_password(password, user)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ошибка верификации! Неверный email или пароль!",
            )

        return RedirectResponse(
            url=request.url_for("web/user_detail", pk=user.id),
            status_code=status.HTTP_302_FOUND,
        )

    except HTTPException as e:
        return templates.TemplateResponse(
            "cafe/login_form.html",
            {
                "request": request,
                "action_url": request.url_for("web/login"),
                "current_email": email,
                "error": f"Ошибка при входе HTTPException: {str(e)}",
            },
            status_code=401,
        )
    except Exception as e:
        return templates.TemplateResponse(
            "cafe/login_form.html",
            {
                "request": request,
                "action_url": request.url_for("web/login"),
                "current_email": email,
                "error": f"Неопознанная Ошибка при входе: {str(e)}",
            },
            status_code=400,
        )
