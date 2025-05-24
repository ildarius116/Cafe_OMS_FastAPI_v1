from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from src.core.models import Base, IdIntPkMixin
from src.core.models.roles import role_permissions

if TYPE_CHECKING:
    from src.core.models import Role


class Permission(Base, IdIntPkMixin):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permissions, back_populates="permissions"
    )

    def __str__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name}, roles={self.roles}>"

    def __repr__(self) -> str:
        return str(self)
