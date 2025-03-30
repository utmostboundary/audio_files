from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException

from app.application.errors import ApplicationError
from app.application.services.auth_service import SignInRequest, AuthenticationService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign_in/")
@inject
async def sign_in(request: SignInRequest, handler: FromDishka[AuthenticationService]):
    try:
        credentials = await handler.sign_in(request=request)
        return credentials
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e)
