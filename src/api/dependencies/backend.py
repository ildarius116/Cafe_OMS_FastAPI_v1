from fastapi_users.authentication import AuthenticationBackend

from .strategy import get_database_strategy
from src.core.authentification.transport import bearer_transport

authentication_backend = AuthenticationBackend(
    name="access_tokens_db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
