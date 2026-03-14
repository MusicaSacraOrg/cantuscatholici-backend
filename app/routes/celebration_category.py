from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.celebration_category import (
    CelebrationCategory,
    CelebrationCategoryCreate,
    CelebrationCategoryUpdate,
)
from app.schemas.user import UserInDb
from app.services.celebration_category import (
    create_celebration_category,
    delete_celebration_category,
    get_celebration_categories,
    get_celebration_category_by_id,
    update_celebration_category,
)

celebration_category_router = APIRouter(
    prefix="/celebration-categories",
    tags=["Celebration Categories"],
    responses={404: {"description": "Not found"}},
)


@celebration_category_router.get("/", response_model=Paginated[CelebrationCategory])
async def list_celebration_categories(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_celebration_categories(db, pagination)


@celebration_category_router.get("/{category_id}", response_model=CelebrationCategory)
async def get_celebration_category(category_id: int, db: DbSessionDep):
    return get_celebration_category_by_id(category_id, db)


@celebration_category_router.post("/", response_model=CelebrationCategory, status_code=201)
async def create_celebration_category_endpoint(
    data: CelebrationCategoryCreate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return create_celebration_category(data, db)


@celebration_category_router.put("/{category_id}", response_model=CelebrationCategory)
async def update_celebration_category_endpoint(
    category_id: int,
    data: CelebrationCategoryUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return update_celebration_category(category_id, data, db)


@celebration_category_router.delete("/{category_id}", response_model=CelebrationCategory)
async def delete_celebration_category_endpoint(
    category_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_celebration_category(category_id, db)

