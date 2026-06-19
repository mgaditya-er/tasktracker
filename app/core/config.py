# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

class Settings(BaseSettings):
    DATABASE_URL: str
    LOG_LEVEL: str
    APP_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(
        f"Missing required environment variables: {e}"
    )