from models.user import UserModel
from fastapi import status
import json
from tests.conftest import DEFAULT_USER_PAYLOAD


def test_define_me(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.get("/api/v1/auth/define-me", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("email") == DEFAULT_USER_PAYLOAD.get("email")
    assert response_data.get("first_name") == DEFAULT_USER_PAYLOAD.get("first_name")


def test_define_me_with_incorrect_token(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}1'}
    response = client.get("/api/v1/auth/define-me", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
