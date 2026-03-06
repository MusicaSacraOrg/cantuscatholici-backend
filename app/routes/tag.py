
from typing import Annotated

from fastapi import APIRouter, Depends

from app.database import DbSessionDep

from ..auth.permissions import required_role
from ..common.deps.pagination import PaginationParamsDep
from ..common.schemas.pagination import Paginated
from ..schemas.tag import Tag as TagSchema
from ..schemas.tag import TagCreate as TagCreateSchema
from ..schemas.user import UserInDb
from ..services.tag import (
    create_tag,
    delete_tag,
    get_tag_by_id,
    get_tags,
    get_tags_by_category,
    update_tag,
)

tag_router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get("/", response_model=Paginated[TagSchema])
async def get_tags_endpoint(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_tags(db, pagination)


@tag_router.get("/{tag_id}", response_model=TagSchema)
async def get_tag_by_id_endpoint(tag_id: int, db: DbSessionDep):
    return {"tag": get_tag_by_id(tag_id, db)}


@tag_router.get("/by-category/{category_tag_id}", response_model=list[TagSchema])
async def get_tags_by_category_id_endpoint(
        category_tag_id: int,
        db: DbSessionDep,
        pagination: PaginationParamsDep,
):
    return get_tags_by_category(category_tag_id, db, pagination)


@tag_router.post("/create", response_model=TagSchema)
async def create_tag_endpoint(
        tag: TagCreateSchema,
        db: DbSessionDep,
        _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return {"tag": create_tag(tag, db)}


@tag_router.put("/update/{tag_id}", response_model=TagSchema)
def update_tag_endpoint(
        tag_id: int,
        tag: TagCreateSchema,
        db: DbSessionDep,
        _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return {"tag": update_tag(tag_id, tag, db)}


@tag_router.delete("/delete/{tag_id}", response_model=TagSchema)
def delete_tag_endpoint(
        tag_id: int,
        db: DbSessionDep,
        _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return {"tag": delete_tag(tag_id, db)}
