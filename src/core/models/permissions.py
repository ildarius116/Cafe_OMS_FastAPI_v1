from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from src.core.models import Base, IdIntPkMixin
from src.core.models.roles import role_permissions

if TYPE_CHECKING:
    from src.core.models import Role


class Permission(Base, IdIntPkMixin):
    __tablename__ = "permissions"

    DEFAULT_USER_PERMISSIONS = [
        ("read_user", "Просмотр профиля пользователя"),
        ("read_all_users", "Просмотр списка пользователей"),
        ("create_user", "Создание пользователей"),
        ("update_user", "Редактирование пользователей"),
        ("delete_user", "Удаление пользователей"),
        ...,
        ("read_role", "Просмотр роли"),
        ("read_all_roles", "Просмотр списка ролей"),
        ("create_role", "Создание роли"),
        ("update_role", "Редактирование роли"),
        ("delete_role", "Удаление роли"),
        ("add_role_to_user", "Добавление роли к пользователю"),
        ("remove_role_from_user", "Удаление роли из пользователя"),
        ...,
        ("read_permission", "Просмотр разрешения"),
        ("read_all_permissions", "Просмотр списка разрешений"),
        ("create_permission", "Создание разрешения"),
        ("update_permission", "Редактирование разрешения"),
        ("delete_permission", "Удаление разрешения"),
        ("add_permission_to_role", "Добавление разрешения к роли"),
        ("remove_permission_from_role", "Удаление разрешения из роли"),
        ...,
        ("read_order", "Просмотр деталей заказа"),
        ("read_all_orders", "Просмотр списка заказов"),
        ("create_order", "Создание заказа"),
        ("update_order", "Редактирование заказа"),
        ("delete_order", "Удаление заказа"),
        ...,
        ("read_menu_item", "Просмотр блюда (элемента Меню)"),
        ("read_all_menu_items", "Просмотр списка блюд"),
        ("create_menu_item", "Создание блюда"),
        ("update_menu_item", "Редактирование блюда"),
        ("delete_menu_item", "Удаление блюда"),
        ("add_menu_item_into_order", "Добавление блюда в заказ"),
        ("del_menu_item_from_order", "Удаление блюда из заказа"),
    ]

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permissions, back_populates="permissions"
    )

    def __str__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name}>"

    def __repr__(self) -> str:
        return str(self)
