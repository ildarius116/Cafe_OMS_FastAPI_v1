from fastapi_users.authentication import BearerTransport
from fastapi_users.authentication import CookieTransport

from src.core.config import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)


cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600,
)
