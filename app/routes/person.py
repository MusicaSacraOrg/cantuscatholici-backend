from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.person import PersonInDb, PersonUpdate
from app.schemas.user import UserInDb
from app.services.person import delete_person, get_person_by_id, get_persons, update_person

person_router = APIRouter(
    prefix="/persons",
    tags=["Persons"],
    responses={404: {"description": "Not found"}},
)


@person_router.get("/", response_model=Paginated[PersonInDb])
async def list_persons(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_persons(db, pagination)


@person_router.get("/{person_id}", response_model=PersonInDb)
async def get_person(person_id: int, db: DbSessionDep):
    return get_person_by_id(person_id, db)


@person_router.put("/{person_id}", response_model=PersonInDb)
async def update_person_endpoint(
    person_id: int,
    data: PersonUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return update_person(person_id, data, db)


@person_router.delete("/{person_id}", response_model=PersonInDb)
async def delete_person_endpoint(
    person_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_person(person_id, db)

