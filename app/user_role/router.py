from fastapi import APIRouter
from sqlalchemy import select

from app.database import DbSessionDep
from app.user_role.models import UserRole
from app.user_role.schema import UserRolesAllSchema

user_role_router = APIRouter(
    prefix="/user_role",
    tags=["User Role"],
    responses={404: {"description": "Not found"}},
)


@user_role_router.get("/", response_model=UserRolesAllSchema)
def get_roles(
    session: DbSessionDep,
    offset: int = 0,
    limit: int = 100,
):
    stmt = select(UserRole).offset(offset).limit(limit)
    roles = session.scalars(stmt).all()
    return {"roles": roles}  # Pydantic handles conversion
