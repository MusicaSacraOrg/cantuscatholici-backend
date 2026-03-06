from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.person import service
from app.person.schema import PersonCreate, PersonInDb, PersonList
from app.user.schema import UserInDb
from app.user.service import get_current_user

person_router = APIRouter(
    prefix="/person",
    tags=["Person"],
    responses={404: {"description": "Not found"}},
)


@person_router.get("/", response_model=PersonList)
def get_persons(
    session: DbSessionDep,
    p: PaginationParamsDep,
):
    return service.get_persons(session, p)


@person_router.get("/{person_id}", response_model=PersonInDb)
def get_person(session: DbSessionDep, person_id: int):
    return service.get_person(session, person_id)


@person_router.post("/", response_model=PersonInDb)
def create_person(
    session: DbSessionDep,
    body: PersonCreate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.create_person(session, body.name, body.surname, body.description)
