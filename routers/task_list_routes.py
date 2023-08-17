from typing import Any, List

from fastapi import APIRouter, Depends, Request

from base.classes import AsyncSessionManager
from base.permissions import JWTBearer
from repos.task_list_repo import TaskListRepository
from repos.task_repo import TaskRepository
from schemas import TaskListModel, TaskModel
from task.services import TaskService
from task_list.services import TaskListService

task_list_router = APIRouter(prefix="/api/v1/task_list", tags=["task-list"])


@task_list_router.post(
    "/", response_model=TaskListModel, dependencies=[Depends(JWTBearer())]
)
async def create_list(request: Request, task_list: TaskListModel) -> Any:
    async with AsyncSessionManager() as session:
        await TaskListService.is_unique_task_list(
            session, task_list, request.state.user
        )
        task_list_obj = await TaskListService.create_task_list(
            session, task_list, request.state.user
        )
        return task_list_obj


@task_list_router.get(
    "/{task_list_name}/",
    response_model=List[TaskModel],
    dependencies=[Depends(JWTBearer())],
)
async def get_task_list(request: Request, task_list_name: str) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListService.get_task_list_obj_by_name_and_user(
            session, task_list_name, request.state.user
        )
        tasks = await TaskListRepository.get_task_list(session, task_list_obj)
        return tasks


@task_list_router.post(
    "/{task_list_name}/add/",
    response_model=TaskModel,
    dependencies=[Depends(JWTBearer())],
)
async def add_task(request: Request, task_list_name: str, task: TaskModel) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListService.get_task_list_obj_by_name_and_user(
            session, task_list_name, request.state.user
        )
        task_obj = await TaskService.create_task(session, task, task_list_obj.id)
        return task_obj


@task_list_router.delete(
    "/{task_list_name}/delete/{task_name}/", dependencies=[Depends(JWTBearer())]
)
async def remove_task(
    request: Request,
    task_name: str,
    task_list_name: str,
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListService.get_task_list_obj_by_name_and_user(
            session, task_list_name, request.state.user
        )
        task_obj = await TaskService.get_task_be_name_and_list(
            session, task_list_obj, task_name
        )
        await TaskRepository.delete_one(task_obj.id, session)
        return "Deleted"


@task_list_router.put(
    "/{task_list_name}/",
    dependencies=[Depends(JWTBearer())],
    response_model=TaskListModel,
)
async def update_task_list(
    request: Request, task_list_name: str, task_list: TaskListModel
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListService.get_task_list_obj_by_name_and_user(
            session, task_list_name, request.state.user
        )
        task_list_obj = await TaskListService.update_task_list(task_list_obj, task_list)
        return task_list_obj


@task_list_router.put(
    "/{task_list_name}/{task_name}/",
    dependencies=[Depends(JWTBearer())],
    response_model=TaskModel,
)
async def update_task(
    request: Request, task_list_name: str, task_name: str, task: TaskModel
) -> Any:
    async with AsyncSessionManager() as session:
        task_list_obj = await TaskListService.get_task_list_obj_by_name_and_user(
            session, task_list_name, request.state.user
        )
        task_obj = await TaskService.get_task_be_name_and_list(
            session, task_list_obj, task_name
        )
        await TaskService.update_task(session, task_obj.id, task)
        return task_obj
