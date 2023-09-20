from pydantic import BaseSettings

from .api import APISettings, api_settings
from .base import env
from .database import database_settings, DatabaseSettings

# from .logging import logging_settings, LoggingSettings
# from .auth import auth_settings, AuthSettings


class Settings(BaseSettings):
    # LOG_LEVEL: str = env.str("LOG_LEVEL", "INFO")
    DATABASE: DatabaseSettings = database_settings
    API: APISettings = api_settings
    # LOG_SETTINGS: dict = logging_settings.config
    # AUTH: AuthSettings = auth_settings


settings = Settings()
