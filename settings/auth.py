from pydantic import BaseSettings
from .base import env


class AuthSettings(BaseSettings):
    AUTH_EMAIL = env.str("AUTH_EMAIL")
    AUTH_PASSWORD = env.str("AUTH_PASSWORD")


auth_settings = AuthSettings()
