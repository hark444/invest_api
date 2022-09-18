from pydantic import BaseSettings
from .base import env


class DatabaseSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URL = f'postgresql://{env.str("PG_USERNAME")}:{env.str("PG_PASSWORD")}@{env.str("PG_HOST")}:{env.int("PG_PORT",5432)}/{env.str("PG_NAME")}'
    SQLALCHEMY_TEST_DATABASE_URL = f'postgresql://{env.str("PG_USERNAME")}:{env.str("PG_PASSWORD")}@{env.str("PG_HOST")}:{env.int("PG_PORT",5432)}/{env.str("TEST_PG_NAME")}'


database_settings = DatabaseSettings()
