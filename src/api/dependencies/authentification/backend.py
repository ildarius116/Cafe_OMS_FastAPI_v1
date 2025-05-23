from fastapi_users.authentication import AuthenticationBackend

from .strategy import get_database_strategy
from src.core.authentification.transport import cookie_transport, bearer_transport

# TODO доделать разделение
authentication_backend_token = AuthenticationBackend(
    name="access_tokens_db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

authentication_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

authentication_backend_cookie = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
