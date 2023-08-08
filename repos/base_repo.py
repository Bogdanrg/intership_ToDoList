from core.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update


class BaseRepository:
    table: Base

    @classmethod
    async def insert_one(cls, session: AsyncSession, **kwargs) -> None:
        new_row = cls.table(**kwargs)
        session.add(new_row)

    @classmethod
    async def delete_one(cls, obj_id: int, session: AsyncSession) -> None:
        query = delete(cls.table).where(cls.table.id == obj_id)
        await session.execute(query)

    @classmethod
    async def update_one(cls, session: AsyncSession, obj_id: int, **kwargs) -> None:
        query = update(cls.table).where(cls.table.id == obj_id).values(**kwargs)
        await session.execute(query)
