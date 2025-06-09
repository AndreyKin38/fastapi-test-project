from fastapi import Depends, Request, security, Security, HTTPException

from sqlalchemy.orm import Session

from client import GoogleClient
from exception import TokenExpiredException, IncorrectTokenException
from repository import TaskRepository, TaskCache, UserRepository
from database import get_db_session
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


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


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client
    )


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


auth = security.HTTPBearer()
# print(auth.__dict__)


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(auth)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_token(token.credentials)

    except TokenExpiredException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    except IncorrectTokenException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    return user_id







