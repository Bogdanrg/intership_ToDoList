from typing import Optional

from pydantic import BaseModel


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
