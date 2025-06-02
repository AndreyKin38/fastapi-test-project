from dataclasses import dataclass

from repository import TaskRepository, TaskCache
from schemas import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_repository: TaskCache

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.cache_repository.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            task_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.cache_repository.set_tasks(task_schema)
            return task_schema

    def create_task(self, task: TaskSchema):
        self.task_repository.create_task(task)




