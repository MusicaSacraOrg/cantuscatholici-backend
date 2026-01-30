from fastapi import APIRouter
from sqlalchemy import func, select

from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleList

user_role_router = APIRouter(
    prefix="/user_role",
    tags=["User Role"],
    responses={404: {"description": "Not found"}},
)


@user_role_router.get("/", response_model=UserRoleList)
def get_roles(
    session: DbSessionDep,
    p: PaginationParamsDep,
):
    stmt = select(UserRole).offset(p.offset).limit(p.limit)
    total = session.scalar(
        select(func.count()).select_from(UserRole),
    )
    roles = session.scalars(stmt).all()
    return {
        "offset": p.offset,
        "limit": p.limit,
        "total": total,
        "items": roles,
    }
