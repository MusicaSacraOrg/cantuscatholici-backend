from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.static_content import StaticContentRead
from app.schemas.user import UserInDb
from app.services.static_content import (
    delete_static_content,
    get_static_content_by_id,
    get_static_contents,
    upload_static_content,
)

static_content_router = APIRouter(
    prefix="/static-content",
    tags=["Static Content"],
    responses={404: {"description": "Not found"}},
)


@static_content_router.get("/", response_model=Paginated[StaticContentRead])
async def list_static_content(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_static_contents(db, pagination)


@static_content_router.get("/{static_content_id}", response_model=StaticContentRead)
async def get_static_content(static_content_id: int, db: DbSessionDep):
    return get_static_content_by_id(static_content_id, db)


@static_content_router.post("/", response_model=StaticContentRead, status_code=201)
async def upload_static_content_endpoint(
    file: UploadFile,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return await upload_static_content(file, db)


@static_content_router.delete("/{static_content_id}", response_model=StaticContentRead)
async def delete_static_content_endpoint(
    static_content_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_static_content(static_content_id, db)
