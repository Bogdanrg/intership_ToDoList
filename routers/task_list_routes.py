from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status

from base.classes import AsyncSessionManager
from base.permissions import jwt_required
from repos.task_list_repo import TaskListRepository
from repos.task_repo import TaskRepository
from schemas import TaskListModel, TaskModel

task_list_router = APIRouter(prefix="/api/v1/task_list", tags=["task-list"])


@task_list_router.post(
    "/", response_model=TaskListModel, dependencies=[Depends(jwt_required)]
)
async def create_list(request: Request, task_list: TaskListModel) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list.name, request.state.user
        )
        if task_list_obj is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task list with the name already exists",
            )
        task_list_obj = await TaskListRepository.insert_one(
            session,
            name=task_list.name,
            active_date=task_list.active_date,
            user=request.state.user,
        )
        return task_list_obj


@task_list_router.get(
    "/{task_list_name}/",
    response_model=List[TaskModel],
    dependencies=[Depends(jwt_required)],
)
async def get_task_list(request: Request, task_list_name: str) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list_name, request.state.user
        )
        if task_list_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        tasks = await TaskListRepository.get_task_list(session, task_list_obj)
        return tasks


@task_list_router.post(
    "/{task_list_name}/add/",
    response_model=TaskModel,
    dependencies=[Depends(jwt_required)],
)
async def add_task(request: Request, task_list_name: str, task: TaskModel) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list_name, request.state.user
        )
        if task_list_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        task = await TaskRepository.insert_one(
            session,
            name=task.name,
            content=task.content,
            list_id=task_list_obj.id,
        )
        return task


@task_list_router.delete(
    "/{task_list_name}/delete/{task_name}/", dependencies=[Depends(jwt_required)]
)
async def remove_task(
    request: Request,
    task_name: str,
    task_list_name: str,
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list_name, request.state.user
        )
        if task_list_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        task_obj = await TaskRepository.get_task_by_name_and_list(
            session, task_name, task_list_obj
        )
        if task_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no tasks with the name in that list",
            )
        await TaskRepository.delete_one(task_obj.id, session)
        return "Deleted"


@task_list_router.put(
    "/{task_list_name}/",
    dependencies=[Depends(jwt_required)],
    response_model=TaskListModel,
)
async def update_task_list(
    request: Request, task_list_name: str, task_list: TaskListModel
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list_name, request.state.user
        )
        if task_list_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        if task_list.name:
            task_list_obj.name = task_list.name
        if task_list.active_date:
            task_list_obj.active_date = task_list.active_date

        return task_list_obj


@task_list_router.put(
    "/{task_list_name}/{task_name}/",
    dependencies=[Depends(jwt_required)],
    response_model=TaskModel,
)
async def update_task(
    request: Request, task_list_name: str, task_name: str, task: TaskModel
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListRepository.get_task_list_by_name_and_user(
            session, task_list_name, request.state.user
        )
        if task_list_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no lists with the name",
            )
        task_obj = await TaskRepository.get_task_by_name_and_list(
            session, task_name, task_list_obj
        )
        if task_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have no tasks with the name in that list",
            )
        await TaskRepository.update_one(
            session, task_obj.id, **task.model_dump(exclude_none=True)
        )
        return task_obj
