from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, UploadFile, Form, HTTPException

from app.application.errors.base import ApplicationError
from app.application.file_manager import FileMetadata
from app.application.services.upload_file import UploadFileHandler, UploadFileRequest

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/upload_audio/")
@inject
async def upload_audio(
    file: Annotated[UploadFile, Form()],
    audio_name: Annotated[str, Form()],
    handler: FromDishka[UploadFileHandler],
) -> None:
    try:
        await handler.execute(
            request=UploadFileRequest(
                audio_name=audio_name,
                file=FileMetadata(
                    payload=file.file,
                    filename=file.filename,
                    content_type=file.content_type,
                ),
            )
        )
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.message)
