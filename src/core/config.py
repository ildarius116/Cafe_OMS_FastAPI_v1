from typing import Annotated
from fastapi import Path
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "cafe.db"


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    debug: bool = True


settings = Settings()
