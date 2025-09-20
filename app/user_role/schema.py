from typing import Annotated

from pydantic import BaseModel
from pydantic.types import StringConstraints

RoleStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class UserRoleSchema(BaseModel):
    id: int
    role: RoleStr


class UserRolesAllSchema(BaseModel):
    roles: list[UserRoleSchema]
