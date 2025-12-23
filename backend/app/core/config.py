from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    APP_NAME: str = "GameHub API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "REST API каталога видеоигр с пользовательскими рецензиями"
    DEBUG: bool = False

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/gamehub"

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
