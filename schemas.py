from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy_utils import Choice


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "Bogdan",
                "email": "bogdan@gmail.com",
                "password": "password",
            }
        }


class SignInModel(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class TokenPairModel(BaseModel):
    access_token: str
    refresh_token: str


class TaskListModel(BaseModel):
    id: Optional[int] = None
    name: str
    active_date: Optional[datetime] = None


class TaskModel(BaseModel):
    id: Optional[int] = None
    name: str
    content: str
    status: Optional[Choice | str] = None
    list_id: Optional[int] = None

    class Config:
        json_encoders = {Choice: lambda c: c.value if type(c) != str else c}
        arbitrary_types_allowed = True
