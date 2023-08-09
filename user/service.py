import datetime

import jwt
from fastapi import HTTPException, Query
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import app_settings
from repos.user_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HasherService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


class JWTService:
    @staticmethod
    async def get_token_pair(username: str) -> dict:
        access_token = await JWTService.encode_access_token(username)
        refresh_token = await JWTService.encode_refresh_token(username)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    @staticmethod
    async def check_credentials(
        session: AsyncSession, username: str, password: str
    ) -> bool:
        user = await UserRepository.get_user_by_username(username, session)
        if not user:
            return False
        if HasherService.verify_password(password, user.password):
            return True
        return False

    @staticmethod
    async def encode_access_token(username: str) -> str:
        access_token = jwt.encode(
            {
                "username": username,
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(minutes=5),
            },
            app_settings.SECRET,
            algorithm=app_settings.ALGORITHM,
        )
        return access_token

    @staticmethod
    async def encode_refresh_token(username: str) -> str:
        refresh_token = jwt.encode(
            {
                "username": username,
                "type": "refresh_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(hours=24),
            },
            app_settings.SECRET,
            algorithm=app_settings.ALGORITHM,
        )
        return refresh_token

    @staticmethod
    async def decode_token(token: str) -> dict | bool:
        try:
            return jwt.decode(
                token,
                app_settings.SECRET,
                algorithms=app_settings.ALGORITHM,
            )
        except jwt.ExpiredSignatureError:
            return False
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return False

    @staticmethod
    async def refresh_access_token(
        session: AsyncSession, refresh_token: str
    ) -> dict | bool:
        payload = await JWTService.decode_token(refresh_token)
        if not payload:
            return False

        user = UserRepository.get_user_by_username(payload.get("username"), session)
        if not user:
            return False

        access_token = await JWTService.encode_access_token(payload.get("username"))

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens


    @staticmethod
    async def login_required(access_token: str = Query()) -> None:

        payload: dict = await JWTService.decode_token(access_token)
        if not payload:
            raise HTTPException(
                "To"
            )
