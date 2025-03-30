from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, Body
from starlette.responses import Response

from app.application.errors.auth import AuthorizationError
from app.application.errors.base import ApplicationError
from app.application.errors.user import UserDoesNotExistError
from app.application.services.user_service import UserService, UpdateUserRequest

router = APIRouter(prefix="/admin", tags=["Auth"])


@router.get("/users/{user_id}/")
@inject
async def get_user(user_id: int, handler: FromDishka[UserService]):
    try:
        return await handler.get_user(user_id=user_id)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.patch("/users/{user_id}/")
@inject
async def update_user(
    user_id: int,
    email: Annotated[str, Body()],
    handler: FromDishka[UserService],
):
    try:
        await handler.update_user(
            request=UpdateUserRequest(
                user_id=user_id,
                email=email,
            )
        )
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.patch("/users/{user_id}/")
@inject
async def delete_user(
    user_id: int,
    handler: FromDishka[UserService],
):
    try:
        await handler.delete_user(user_id=user_id)
        return Response(status_code=204)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AuthorizationError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.message)
