from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./cafe.db"
    debug: bool = True


settings = Settings()
