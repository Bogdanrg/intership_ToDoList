import motor.motor_asyncio

from config import app_settings

client = motor.motor_asyncio.AsyncIOMotorClient(app_settings.MONGODB_URL)
db = client[app_settings.MONGO_INITDB_DATABASE]
