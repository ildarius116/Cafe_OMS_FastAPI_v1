from fastapi_users.db import SQLAlchemyBaseUserTable

from src.core.models import Base


class UserModel(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
