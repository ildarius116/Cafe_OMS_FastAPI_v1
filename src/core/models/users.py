from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from src.core.models import Base, IdIntPkMixin
from src.core.models.roles import user_roles
from src.core.types.user_id import UserIdType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.core.models import Role


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
