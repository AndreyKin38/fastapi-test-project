from fastapi import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

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


@router.get(
    "/login/google",
    response_class=RedirectResponse
)
async def google_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    "/google"
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse
)
async def yandex_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    "/yandex"
)
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.yandex_auth(code=code)






