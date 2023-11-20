from repos.base_repo import BaseRepository
from core.database import db


class PhoneRepository(BaseRepository):
    collection = db["phone"]
