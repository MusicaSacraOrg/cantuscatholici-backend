from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response

from app.database import DbSessionDep
from app.static_content import service
from app.static_content.exceptions import FileTooLargeException
from app.user.schema import UserInDb
from app.user.service import get_current_user

CONTENT_TYPE_MAP = {
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
    "mscz": "application/octet-stream",
    "mp3": "audio/mpeg",
}

static_content_router = APIRouter(
    prefix="/static_content",
    tags=["Content"],
    responses={404: {"description": "Not found"}},
)


@static_content_router.post("/upload")
def upload_file(
    session: DbSessionDep,
    file: UploadFile,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    content = file.file.read()
    if len(content) > service.MAX_FILE_SIZE:
        raise FileTooLargeException(
            f"File too large. Maximum size: {service.MAX_FILE_SIZE // (1024*1024)} MB"
        )
    return service.store_file(session, file.filename or "unknown", content)


@static_content_router.get("/{file_id}")
def get_file(session: DbSessionDep, file_id: int):
    data, ext = service.get_file(session, file_id)
    content_type = CONTENT_TYPE_MAP.get(ext, "application/octet-stream")
    return Response(content=data, media_type=content_type)


@static_content_router.delete("/{file_id}", status_code=204)
def delete_file(
    session: DbSessionDep,
    file_id: int,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    service.delete_file(session, file_id)
