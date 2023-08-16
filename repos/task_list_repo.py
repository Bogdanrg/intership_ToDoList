from typing import Any

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from task_list.models import TaskList
from user.models import User

from repos.base_repo import BaseRepository


class TaskListRepository(BaseRepository):
    table = TaskList

    @classmethod
    async def get_task_list_by_name_and_user(
        cls, session: AsyncSession, name: str, user: User
    ) -> Result[TaskList]:
        query = select(TaskList).where(
            (TaskList.name == name) & (TaskList.user_id == user.id)
        )
        task_list = await session.execute(query)
        return task_list.scalar_one_or_none()

    @classmethod
    async def get_task_list(
        cls, session: AsyncSession, task_list: TaskList
    ) -> Result[Any]:
        query = (
            select(TaskList)
            .where(TaskList.id == task_list.id)
            .options(selectinload(TaskList.tasks))
        )
        tasks = await session.execute(query)
        return tasks.scalars().first().tasks
