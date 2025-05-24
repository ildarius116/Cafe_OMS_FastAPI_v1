from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.core.models import Base, IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models import Permission, User


class Role(Base, IdIntPkMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))

    permission: Mapped["Permission"] = relationship(back_populates="permissions")
    user: Mapped["User"] = relationship(back_populates="users")
