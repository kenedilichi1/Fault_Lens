from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import getenv

class Settings(BaseSettings):
    app_name: str = 'FaultLens API'

    debug: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


    model_config = SettingsConfigDict(
        env_file=getenv("ENV_FILE", ".env"),
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """Get Settings instance with caching"""
    return Settings()

settings = get_settings()