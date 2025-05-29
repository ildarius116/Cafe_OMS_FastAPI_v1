import logging
from typing import Optional, TYPE_CHECKING, Union
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.password import PasswordHelper

from src.core.config import settings
from src.core.models import User
from src.core.schemas.users import UserCreate
from src.core.types.user_id import UserIdType

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)
password_helper = PasswordHelper()


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret: str = settings.access_token.reset_password_token_secret
    verification_token_secret: str = settings.access_token.verification_token_secret

    async def validate_password(
        self,
        password: str,
        user: Union[User, UserCreate],
    ) -> bool:
        if isinstance(user, UserCreate):
            return bool(password)

        is_valid = password_helper.verify_and_update(password, user.hashed_password)
        if is_valid[0]:
            log.warning(
                "User %r is validated.",
                user.email,
            )
        else:
            log.warning(
                "User %r is NOT validated.",
                user.email,
            )

        return is_valid[0]

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
