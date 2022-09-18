# configuration for unit tests
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient

# from app.auth.inter_service_auth import verify_auth_token
from models.user import UserModel
from settings import settings
from models import Base, get_db
from main import application
import json


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(settings.DATABASE.SQLALCHEMY_TEST_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    testing_session_factory = sessionmaker(
        autoflush=False, autocommit=False, bind=db_engine
    )
    try:
        session = testing_session_factory()
        yield session
    finally:
        clear_db(session)
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    application.dependency_overrides[get_db] = lambda: db_session

    with TestClient(application) as client:
        yield client


def clear_db(session):
    session.query(UserModel).delete()
    session.commit()


DEFAULT_USER_PAYLOAD = {
    "email": "test@gmail.com",
    "password": "Test@123",
    "first_name": "Test",
    "last_name": "User",
}


@pytest.fixture(scope="function")
def account_user_and_token(client):
    response = client.post(f"/api/v1/users/create", data=DEFAULT_USER_PAYLOAD)
    if response.status_code == 200:
        user_id = response.json().get("id")
        response = client.post(f"/api/v1/auth/token", data=DEFAULT_USER_PAYLOAD)
        if response.status_code == 200:
            return {
                "user_id": user_id,
                "access_token": response.json().get("access_token"),
            }
