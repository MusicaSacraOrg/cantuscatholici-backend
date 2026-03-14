from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.author import Author, AuthorCreate, AuthorUpdate
from app.schemas.user import UserInDb
from app.services.author import (
    create_author,
    delete_author,
    get_author_by_id,
    get_authors,
    update_author,
)

author_router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
    responses={404: {"description": "Not found"}},
)


@author_router.get("/", response_model=Paginated[Author])
async def list_authors(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_authors(db, pagination)


@author_router.get("/{author_id}", response_model=Author)
async def get_author(author_id: int, db: DbSessionDep):
    return get_author_by_id(author_id, db)


@author_router.post("/", response_model=Author, status_code=201)
async def create_author_endpoint(
    data: AuthorCreate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return create_author(data, current_user.id, db)


@author_router.put("/{author_id}", response_model=Author)
async def update_author_endpoint(
    author_id: int,
    data: AuthorUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return update_author(author_id, data, db)


@author_router.delete("/{author_id}", response_model=Author)
async def delete_author_endpoint(
    author_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_author(author_id, db)

