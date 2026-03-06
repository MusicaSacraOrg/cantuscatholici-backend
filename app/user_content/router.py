from typing import Annotated

from fastapi import APIRouter, Depends

from app.database import DbSessionDep
from app.user.schema import UserInDb
from app.user.service import get_current_user
from app.user_content import service
from app.user_content.schema import (
    UserContentCreate,
    UserContentListResponse,
    UserContentRead,
    UserContentUpdate,
)

user_content_router = APIRouter(
    tags=["User Content"],
    responses={404: {"description": "Not found"}},
)


@user_content_router.get(
    "/song/{song_id}/content", response_model=UserContentListResponse
)
def get_song_content(session: DbSessionDep, song_id: int):
    return service.get_song_user_content(session, song_id)


@user_content_router.post(
    "/song/{song_id}/content", response_model=UserContentRead
)
def create_song_content(
    session: DbSessionDep,
    song_id: int,
    body: UserContentCreate,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.create_user_content(
        session,
        song_id=song_id,
        user_id=current_user.id,
        title=body.title,
        description=body.description,
        content_type=body.content_type,
        file_id=body.file_id,
        mscz_id=body.mscz_id,
    )


@user_content_router.get(
    "/user-content/{uc_id}", response_model=UserContentRead
)
def get_content_detail(session: DbSessionDep, uc_id: int):
    return service.get_user_content(session, uc_id)


@user_content_router.put(
    "/user-content/{uc_id}", response_model=UserContentRead
)
def update_content(
    session: DbSessionDep,
    uc_id: int,
    body: UserContentUpdate,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.update_user_content(
        session,
        uc_id=uc_id,
        user_id=current_user.id,
        title=body.title,
        description=body.description,
        content_type=body.content_type,
    )


@user_content_router.delete("/user-content/{uc_id}", status_code=204)
def delete_content(
    session: DbSessionDep,
    uc_id: int,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    service.delete_user_content(session, uc_id, current_user.id)
