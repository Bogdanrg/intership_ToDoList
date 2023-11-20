from typing import List

from core.database import db


class BaseRepository:
    collection: db

    @classmethod
    async def create(cls, data: dict) -> None:
        data.update({"count": 0})
        await cls.collection.insert_one(data)

    @classmethod
    async def increase_count(cls, document_id: str) -> None:
        document = await cls.collection.find_one({"id": document_id})
        await cls.collection.update_one({"id": document_id}, {"$set": {"count": document['count'] + 1}})

    @classmethod
    async def get_all(cls) -> List[dict]:
        documents = cls.collection.find({}, {"_id": False}).sort("count", -1)
        document_list = await documents.to_list(1000)
        return document_list
