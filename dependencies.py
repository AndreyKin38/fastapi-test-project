from fastapi import Depends

from repository import TaskRepository, TaskCache
from database import get_db_session
from cache import get_redis_connection
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_tasks_repository() -> TaskCache:
    redis = get_redis_connection()
    return TaskCache(redis)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        cache_repository: TaskCache = Depends(get_cache_tasks_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        cache_repository=cache_repository
    )
