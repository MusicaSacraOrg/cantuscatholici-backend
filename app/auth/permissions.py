from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated

from ..common.exceptions import ForbiddenException
from ..schemas.user import UserInDb
from ..services.user import get_current_user

ROLE_RANK: dict[str, int] = {
    "User": 1,
    "Redactor": 2,
    "Admin": 3,
}


def required_role(min_role: str) -> Callable:
    async def role_dependency(
        current_user: Annotated[UserInDb, Depends(get_current_user)],
    ) -> UserInDb:
        user_rank = ROLE_RANK.get(current_user.role)
        required_rank = ROLE_RANK.get(min_role)

        if user_rank is None or required_rank is None:
            raise ForbiddenException()

        if user_rank < required_rank:
            raise ForbiddenException()

        return current_user

    return role_dependency
