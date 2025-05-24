from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from src.core.models import Base, IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models import Permission, User


class Role(Base, IdIntPkMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    permissions: Mapped[List["Permission"]] = relationship(back_populates="permissions")
    user: Mapped["User"] = relationship(back_populates="users")
