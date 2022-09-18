from pydantic import BaseModel
from typing import Optional
from fastapi.param_functions import Form


class UserSchemaForm:
    def __init__(
        self,
        email: str = Form(),
        password: str = Form(),
        first_name: Optional[str] = Form(default=None),
        last_name: Optional[str] = Form(default=None),
        disabled: bool = Form(default=False),
    ):
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.disabled = disabled


class UserUpdateSchemaForm:
    def __init__(
        self,
        email: str = Form(default=None),
        password: str = Form(default=None),
        first_name: Optional[str] = Form(default=None),
        last_name: Optional[str] = Form(default=None),
        disabled: bool = Form(default=False),
    ):
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.disabled = disabled

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "disabled": self.disabled,
        }
