from dataclasses import dataclass

from app.exception import TaskNotFound
from app.tasks.repository import TaskRepository, TaskCache
from app.tasks.schemas import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_repository: TaskCache

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := await self.cache_repository.get_tasks():
            return tasks
        else:
            tasks = await self.task_repository.get_tasks()
            task_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.cache_repository.set_tasks(task_schema)
            return task_schema

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(task, user_id)
        task = await self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)




