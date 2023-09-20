from pydantic import BaseSettings
from .base import env


class APISettings(BaseSettings):
    LOCALHOST = env.str("LOCALHOST")
    LOCAL_PORT = env.int("LOCAL_PORT")
    SQLALCHEMY_TEST_DATABASE_URL = f'postgresql://{env.str("PG_USERNAME")}:{env.str("PG_PASSWORD")}@{env.str("PG_HOST")}:{env.int("PG_PORT",5432)}/{env.str("TEST_PG_NAME")}'


api_settings = APISettings()
