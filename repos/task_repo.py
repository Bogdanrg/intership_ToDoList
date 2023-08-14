from typing import Any

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from task.models import Task
from task_list.models import TaskList

from .base_repo import BaseRepository


class TaskRepository(BaseRepository):
    table = Task

    @classmethod
    async def get_task_by_name_and_list(
        cls, session: AsyncSession, task_name: str, task_list: TaskList
    ) -> Result[Any] | None:
        query = select(Task).where(
            (Task.list_id == task_list.id) & (Task.name == task_name)
        )
        task = await session.execute(query)
        return task.scalar_one_or_none()
