from fastapi import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies import get_auth_service
from exception import UserNotFoundException, PasswordErrorException
from schemas import UserLoginSchema, UserCreateSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserLoginSchema:
    try:
        return auth_service.login(username=body.username, password=body.password)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except PasswordErrorException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


