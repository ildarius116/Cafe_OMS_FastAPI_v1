from fastapi_users import FastAPIUsers

from src.api.dependencies.authentification.backend import authentication_backend
from src.api.dependencies.authentification.user_manager import get_user_manager
from src.core.models import User
from src.core.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
