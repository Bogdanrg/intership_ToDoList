from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from config import app_settings
from routers.auth_routes import auth_router
from base.middleware import AuthMiddleware

app = FastAPI(title=app_settings.APP_TITLE)

app.include_router(auth_router)

auth_middleware = AuthMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
