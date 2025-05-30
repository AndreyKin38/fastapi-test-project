from typing import Annotated

from fastapi import APIRouter, status, Depends

from schemas import TaskSchema
from repository import TaskRepository
from dependencies import get_task_service, get_tasks_repository
from service import TaskService

router = APIRouter(prefix="/tasks",
                   tags=["tasks"])


@router.get(
    "/all_tasks",
    response_model=list[TaskSchema]
)
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()


@router.post(
    "/",
    response_model=TaskSchema
)
async def create_task(
        task: TaskSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    task_id = task_service.create_task(task)
    task.id = task_id
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema
)
async def patch_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    return task_repository.update_task_name(task_id, name)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    return task_repository.delete_task(task_id)


@router.get("/task")
async def get_task(task_id: int) -> TaskSchema:
    pass



