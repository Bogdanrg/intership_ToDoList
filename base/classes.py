import logging

from core.database import async_session


class AsyncSessionManager:
    def __init__(self):
        self.session = async_session()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(f"Exception occurred, type: {exc_type}, value: {exc_val}")
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
