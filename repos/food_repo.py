from repos.base_repo import BaseRepository
from core.database import db


class FoodRepository(BaseRepository):
    collection = db["food"]
