from fastapi import HTTPException
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import Base
from repos.task_list_repo import TaskListRepository
from schemas import TaskListModel
from task_list.models import TaskList
from user.models import User


class TaskListService:
    @staticmethod
    async def get_task_list_obj_by_name_and_user(session: AsyncSession, task_list: str, user: User) -> Result[TaskList]:
        task_list = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list, user
        )
        if task_list is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        return task_list

    @staticmethod
    async def is_unique_task_list(session: AsyncSession, task_list: TaskListModel, user: User) -> None:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list.name, user
        )
        if task_list_obj is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task list with the name already exists",
            )

    @staticmethod
    async def create_task_list(session: AsyncSession, task_list: TaskListModel, user: User) -> Base:
        task_list = await TaskListRepository.insert_one(
            session,
            name=task_list.name,
            active_date=task_list.active_date,
            user=user
        )
        return task_list

    @staticmethod
    async def update_task_list(task_list_obj: TaskList, task_list: TaskListModel) -> TaskList:
        if task_list.name:
            task_list_obj.name = task_list.name
        if task_list.active_date:
            task_list_obj.active_date = task_list.active_date
        return task_list_obj
