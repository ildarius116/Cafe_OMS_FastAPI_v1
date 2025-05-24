from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from src.core.models import Base, IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models import Role


class Permission(Base, IdIntPkMixin):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    roles: Mapped[List["Role"]] = relationship(back_populates="permission")
