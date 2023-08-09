from fastapi import Request, HTTPException
from user.service import JWTService
from repos.user_repo import UserRepository
from base.classes import AsyncSessionManager


class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        print(request.url)
        token_exception = HTTPException(
            status_code=400,
            detail="Token wasn't provided"
        )
        async with AsyncSessionManager() as session:
            token = request.headers.get("JWT")
            if not token:
                return token_exception
            payload = await JWTService.decode_token(token)
            if not payload:
                return HTTPException(
                    status_code=400,
                    detail="Invalid token"
                )
            user = await UserRepository.get_user_by_username(payload.get("username"), session)
            if not user:
                return token_exception
            setattr(request, "user", user)
            response = await call_next(request)
            return response
