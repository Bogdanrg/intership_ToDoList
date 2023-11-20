from fastapi import FastAPI
from config import app_settings
from api.v1.analytical_routes import analytical_router


app = FastAPI(title=app_settings.APP_TITLE)

app.include_router(analytical_router)
