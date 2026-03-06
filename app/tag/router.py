from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.tag import service
from app.tag.schema import TagCreate, TagList, TagRead, TagUpdate
from app.user.schema import UserInDb
from app.user.service import get_current_user

tag_router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get("/", response_model=TagList)
def get_tags(
    session: DbSessionDep,
    p: PaginationParamsDep,
    category_id: int | None = Query(default=None),
):
    return service.get_tags(session, p, category_id=category_id)


@tag_router.get("/{tag_id}", response_model=TagRead)
def get_tag(session: DbSessionDep, tag_id: int):
    return service.get_tag(session, tag_id)


@tag_router.post("/", response_model=TagRead)
def create_tag(
    session: DbSessionDep,
    body: TagCreate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.create_tag(session, body.name, body.category_id)


@tag_router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    session: DbSessionDep,
    tag_id: int,
    body: TagUpdate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.update_tag(session, tag_id, body.name, body.category_id)


@tag_router.delete("/{tag_id}", status_code=204)
def delete_tag(
    session: DbSessionDep,
    tag_id: int,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    service.delete_tag(session, tag_id)
