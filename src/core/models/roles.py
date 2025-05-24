from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from src.core.models import Base, IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models import Permission, User

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id"),
        primary_key=True,
    ),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
)


class Role(Base, IdIntPkMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permissions,
        back_populates="roles",
    )
    users: Mapped[List["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
    )

    def __str__(self) -> str:
        return (
            f"<Role(id={self.id}, "
            f"name={self.name}, "
            f"user={self.users}, "
            f"roles={self.permissions}>"
        )

    def __repr__(self) -> str:
        return str(self)
