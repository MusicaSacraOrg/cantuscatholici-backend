from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.tag_category import service
from app.tag_category.schema import (
    TagCategoryCreate,
    TagCategoryList,
    TagCategoryRead,
    TagCategoryUpdate,
    TagCategoryWithTags,
)
from app.user.schema import UserInDb
from app.user.service import get_current_user

tag_category_router = APIRouter(
    prefix="/tag_category",
    tags=["Tag Category"],
    responses={404: {"description": "Not found"}},
)


@tag_category_router.get("/", response_model=TagCategoryList)
def get_tag_categories(
    session: DbSessionDep,
    p: PaginationParamsDep,
):
    return service.get_tag_categories(session, p)


@tag_category_router.get("/with-tags", response_model=list[TagCategoryWithTags])
def get_all_with_tags(session: DbSessionDep):
    return service.get_all_with_tags(session)


@tag_category_router.get("/{category_id}", response_model=TagCategoryRead)
def get_tag_category(session: DbSessionDep, category_id: int):
    return service.get_tag_category(session, category_id)


@tag_category_router.post("/", response_model=TagCategoryRead)
def create_tag_category(
    session: DbSessionDep,
    body: TagCategoryCreate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.create_tag_category(session, body.name, body.color)


@tag_category_router.put("/{category_id}", response_model=TagCategoryRead)
def update_tag_category(
    session: DbSessionDep,
    category_id: int,
    body: TagCategoryUpdate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.update_tag_category(session, category_id, body.name, body.color)


@tag_category_router.delete("/{category_id}", status_code=204)
def delete_tag_category(
    session: DbSessionDep,
    category_id: int,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    service.delete_tag_category(session, category_id)
