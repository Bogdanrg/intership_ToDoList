import motor.motor_asyncio

from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo.MONGO_URL)
db = client[settings.mongo.MONGO_INITDB_DATABASE]
