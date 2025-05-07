from typing import Annotated
from fastapi import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./cafe.db"
    debug: bool = True
    pk_type = Annotated[int, Path(ge=1, lt=1_000_000)]


settings = Settings()
