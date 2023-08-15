from fastapi import HTTPException, Request

from repos.user_repo import UserRepository
from user.service import JWTService

from .classes import AsyncSessionManager
from .services import AuthService


async def jwt_required(request: Request):
    async with AsyncSessionManager() as session:
        token = AuthService.get_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="Token wasn't provided")
        payload = await JWTService.decode_token(token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = await UserRepository.get_user_by_username(
            payload.get("username", ""), session
        )
        if not user:
            raise HTTPException(status_code=400, detail="Invalid token")
        request.state.user = user
