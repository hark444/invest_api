from models.user import RoleTypeEnum
from fastapi import status


def test_default_user_role_is_regular(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.get("/api/v1/auth/define-me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data.get("role") == RoleTypeEnum.regular


def test_role_is_getting_updated(client, account_user_and_token):
    user_id = account_user_and_token.get("user_id")
    payload = {"role": RoleTypeEnum.admin}
    response = client.patch(f"/api/v1/user-role/{user_id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data.get("role") == RoleTypeEnum.admin


def test_role_update_with_missing_data(client, account_user_and_token):
    user_id = account_user_and_token.get("user_id")
    response = client.patch(f"/api/v1/user-role/{user_id}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data == {
        "detail": [
            {"loc": ["body"], "msg": "field required", "type": "value_error.missing"}
        ]
    }
