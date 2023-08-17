from fastapi import HTTPException
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import Base
from repos.task_repo import TaskRepository
from schemas import TaskModel
from task.models import Task
from task_list.models import TaskList


class TaskService:
    @staticmethod
    async def create_task(
        session: AsyncSession, task: TaskModel, task_list_obj_id: int
    ) -> Base:
        task = await TaskRepository.insert_one(
            session,
            name=task.name,
            content=task.content,
            status=task.status,
            list_id=task_list_obj_id,
        )
        return task

    @staticmethod
    async def get_task_be_name_and_list(
        session: AsyncSession, task_list_obj: TaskList, task_name: str
    ) -> Result[Task]:
        task = await TaskRepository.get_task_by_name_and_list(
            session, task_name, task_list_obj
        )
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no tasks with the name in that list",
            )
        return task

    @staticmethod
    async def update_task(
        session: AsyncSession, task_obj_id: int, task: TaskModel
    ) -> None:
        await TaskRepository.update_one(
            session, task_obj_id, **task.model_dump(exclude_none=True)
        )
