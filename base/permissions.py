from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from base.classes import AsyncSessionManager
from repos.user_repo import UserRepository
from user.service import JWTService


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):
        async with AsyncSessionManager() as session:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
                payload: dict | None = await JWTService.decode_token(credentials.credentials)
                if not payload:
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                request.state.user = await UserRepository.get_user_by_username(payload["username"], session)
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")
