from typing import Annotated
from fastapi import Path
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "cafe.db"
DB_TEST_PATH = BASE_DIR / "test_cafe.db"


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    web_prefix: str = ""

    db_url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    db_test_url: str = f"sqlite+aiosqlite:///{DB_TEST_PATH}"
    debug: bool = True

    ORDER_STATUSES: dict = {
        "pending": "В ожидании",
        "ready": "Готово",
        "paid": "Оплачено",
    }

    MENU_ITEM_TYPES: dict = {
        "not assigned": "Не назначено",
        "first courses": "Первые блюда",
        "second courses": "Вторые блюда",
        "garnishes": "Гарниры",
        "salads": "Салаты",
        "desserts": "Десерты",
        "cold drinks": "Холодные напитки",
        "hot drinks": "Горячие напитки",
        "others": "Прочее",
    }


settings = Settings()
