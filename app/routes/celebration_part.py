from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.celebration_part import (
    CelebrationPart,
    CelebrationPartCreate,
    CelebrationPartUpdate,
)
from app.schemas.user import UserInDb
from app.services.celebration_part import (
    create_celebration_part,
    delete_celebration_part,
    get_celebration_part_by_id,
    get_celebration_parts,
    update_celebration_part,
)

celebration_part_router = APIRouter(
    prefix="/celebration-parts",
    tags=["Celebration Parts"],
    responses={404: {"description": "Not found"}},
)


@celebration_part_router.get("/", response_model=Paginated[CelebrationPart])
async def list_celebration_parts(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_celebration_parts(db, pagination)


@celebration_part_router.get("/{part_id}", response_model=CelebrationPart)
async def get_celebration_part(part_id: int, db: DbSessionDep):
    return get_celebration_part_by_id(part_id, db)


@celebration_part_router.post("/", response_model=CelebrationPart, status_code=201)
async def create_celebration_part_endpoint(
    data: CelebrationPartCreate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return create_celebration_part(data, db)


@celebration_part_router.put("/{part_id}", response_model=CelebrationPart)
async def update_celebration_part_endpoint(
    part_id: int,
    data: CelebrationPartUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return update_celebration_part(part_id, data, db)


@celebration_part_router.delete("/{part_id}", response_model=CelebrationPart)
async def delete_celebration_part_endpoint(
    part_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_celebration_part(part_id, db)

