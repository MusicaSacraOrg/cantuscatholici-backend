from typing import Annotated

from fastapi import Depends, HTTPException

from app.user.schema import UserInDb
from app.user.service import get_current_user


def require_role(*roles: str):
    async def dependency(
        current_user: Annotated[UserInDb, Depends(get_current_user)],
    ) -> UserInDb:
        if current_user.role not in roles:
            raise HTTPException(403, "Insufficient permissions")
        return current_user

    return dependency
