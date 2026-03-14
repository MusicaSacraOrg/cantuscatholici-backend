from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.celebration import (
    Celebration,
    CelebrationCreate,
    CelebrationSong,
    CelebrationSongCreate,
    CelebrationSongUpdate,
    CelebrationUpdate,
)
from app.schemas.user import UserInDb
from app.services.celebration import (
    create_celebration,
    create_celebration_song,
    delete_celebration,
    delete_celebration_song,
    get_celebration_by_id,
    get_celebration_song_by_id,
    get_celebration_songs,
    get_celebrations,
    update_celebration,
    update_celebration_song,
)

celebration_router = APIRouter(
    prefix="/celebrations",
    tags=["Celebrations"],
    responses={404: {"description": "Not found"}},
)


@celebration_router.get("/", response_model=Paginated[Celebration])
async def list_celebrations(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_celebrations(db, pagination)


@celebration_router.get("/{celebration_id}", response_model=Celebration)
async def get_celebration(celebration_id: int, db: DbSessionDep):
    return get_celebration_by_id(celebration_id, db)


@celebration_router.post("/", response_model=Celebration, status_code=201)
async def create_celebration_endpoint(
    data: CelebrationCreate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return create_celebration(data, db)


@celebration_router.put("/{celebration_id}", response_model=Celebration)
async def update_celebration_endpoint(
    celebration_id: int,
    data: CelebrationUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return update_celebration(celebration_id, data, db)


@celebration_router.delete("/{celebration_id}", response_model=Celebration)
async def delete_celebration_endpoint(
    celebration_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_celebration(celebration_id, db)


# --- Celebration Songs ---

@celebration_router.get(
    "/{celebration_id}/songs",
    response_model=Paginated[CelebrationSong],
)
async def list_celebration_songs(
    celebration_id: int, db: DbSessionDep, pagination: PaginationParamsDep,
):
    return get_celebration_songs(celebration_id, db, pagination)


@celebration_router.get(
    "/{celebration_id}/songs/{celebration_song_id}",
    response_model=CelebrationSong,
)
async def get_celebration_song(
    celebration_id: int,  # noqa: ARG001
    celebration_song_id: int,
    db: DbSessionDep,
):
    return get_celebration_song_by_id(celebration_song_id, db)


@celebration_router.post(
    "/{celebration_id}/songs",
    response_model=CelebrationSong,
    status_code=201,
)
async def create_celebration_song_endpoint(
    celebration_id: int,
    data: CelebrationSongCreate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return create_celebration_song(celebration_id, data, db)


@celebration_router.put(
    "/{celebration_id}/songs/{celebration_song_id}",
    response_model=CelebrationSong,
)
async def update_celebration_song_endpoint(
    celebration_id: int,  # noqa: ARG001
    celebration_song_id: int,
    data: CelebrationSongUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return update_celebration_song(celebration_song_id, data, db)


@celebration_router.delete(
    "/{celebration_id}/songs/{celebration_song_id}",
    response_model=CelebrationSong,
)
async def delete_celebration_song_endpoint(
    celebration_id: int,  # noqa: ARG001
    celebration_song_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return delete_celebration_song(celebration_song_id, db)

