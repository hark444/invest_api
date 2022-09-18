from models.user import UserModel
from fastapi import status
import json

DEFAULT_USER_PAYLOAD = {
    "email": "hkeshwani68@gmail.com",
    "password": "Test@123",
    "first_name": "Harshad",
    "last_name": "Keshwani",
}


def test_create_user(client):
    response = client.post(f"/api/v1/users/create", data=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)
    assert response_data.get("email") == DEFAULT_USER_PAYLOAD.get("email")
    assert not response_data.get("disabled")


def test_create_user_with_missing_email(client):
    del DEFAULT_USER_PAYLOAD["email"]
    response = client.post(f"/api/v1/users/create", data=DEFAULT_USER_PAYLOAD)
    response_data = json.loads(response.text)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
