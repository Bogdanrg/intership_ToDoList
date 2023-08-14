from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from base.middleware import AuthMiddleware
from config import app_settings
from routers.auth_routes import auth_router
from routers.task_list_routes import task_list_router

app = FastAPI(title=app_settings.APP_TITLE)

app.include_router(auth_router)
app.include_router(task_list_router)

auth_middleware = AuthMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
