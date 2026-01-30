from typing import Annotated

from pydantic import BaseModel
from pydantic.types import StringConstraints

from app.common.schemas.pagination import Paginated

RoleStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class UserRoleInDb(BaseModel):
    id: int
    role: RoleStr


class UserRoleList(Paginated[UserRoleInDb]):
    pass
