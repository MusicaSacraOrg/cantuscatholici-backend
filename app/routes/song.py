from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.song import (
    Song,
    SongArrangement,
    SongArrangementCreate,
    SongArrangementUpdate,
    SongCreate,
    SongFilterParams,
    SongPart,
    SongPartCreate,
    SongPartUpdate,
    SongScoreRead,
    SongUpdate,
)
from app.schemas.user import UserInDb
from app.services.song import (
    create_song,
    create_song_arrangement,
    create_song_part,
    create_song_score,
    delete_song,
    delete_song_arrangement,
    delete_song_part,
    delete_song_score,
    filter_songs,
    get_song_arrangement_by_id,
    get_song_arrangements,
    get_song_by_id,
    get_song_part_by_id,
    get_song_parts,
    get_song_score,
    get_songs,
    update_song,
    update_song_arrangement,
    update_song_part,
)

song_router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
    responses={404: {"description": "Not found"}},
)

# --- Songs ---

@song_router.get("/", response_model=Paginated[Song])
async def list_songs(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_songs(db, pagination)


@song_router.post("/filter", response_model=Paginated[Song])
async def filter_songs_endpoint(
    params: SongFilterParams,
    db: DbSessionDep,
    pagination: PaginationParamsDep,
):
    return filter_songs(params, db, pagination)


@song_router.get("/{song_id}", response_model=Song)
async def get_song(song_id: int, db: DbSessionDep):
    return get_song_by_id(song_id, db)


@song_router.post("/", response_model=Song, status_code=201)
async def create_song_endpoint(
    data: SongCreate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return create_song(data, current_user.id, db)


@song_router.put("/{song_id}", response_model=Song)
async def update_song_endpoint(
    song_id: int,
    data: SongUpdate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return update_song(song_id, data, current_user.id, db)


@song_router.delete("/{song_id}", response_model=Song)
async def delete_song_endpoint(
    song_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return delete_song(song_id, db)


# --- Song Parts ---

@song_router.get("/{song_id}/parts", response_model=list[SongPart])
async def list_song_parts(song_id: int, db: DbSessionDep):
    return get_song_parts(song_id, db)


@song_router.get("/{song_id}/parts/{part_id}", response_model=SongPart)
async def get_song_part(song_id: int, part_id: int, db: DbSessionDep):  # noqa: ARG001
    return get_song_part_by_id(part_id, db)


@song_router.post("/{song_id}/parts", response_model=SongPart, status_code=201)
async def create_song_part_endpoint(
    song_id: int,
    data: SongPartCreate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return create_song_part(song_id, data, db)


@song_router.put("/{song_id}/parts/{part_id}", response_model=SongPart)
async def update_song_part_endpoint(
    song_id: int,  # noqa: ARG001
    part_id: int,
    data: SongPartUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return update_song_part(part_id, data, db)


@song_router.delete("/{song_id}/parts/{part_id}", response_model=SongPart)
async def delete_song_part_endpoint(
    song_id: int,  # noqa: ARG001
    part_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return delete_song_part(part_id, db)


# --- Song Score ---

@song_router.get("/{song_id}/score", response_model=SongScoreRead)
async def get_song_score_endpoint(song_id: int, db: DbSessionDep):
    return get_song_score(song_id, db)


@song_router.post("/{song_id}/score", response_model=SongScoreRead, status_code=201)
async def create_song_score_endpoint(
    song_id: int,
    static_content_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return create_song_score(song_id, static_content_id, db)


@song_router.delete("/{song_id}/score", response_model=SongScoreRead)
async def delete_song_score_endpoint(
    song_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return delete_song_score(song_id, db)


# --- Song Arrangements ---

@song_router.get("/{song_id}/arrangements", response_model=Paginated[SongArrangement])
async def list_song_arrangements(
    song_id: int, db: DbSessionDep, pagination: PaginationParamsDep,
):
    return get_song_arrangements(song_id, db, pagination)


@song_router.get("/{song_id}/arrangements/{arrangement_id}", response_model=SongArrangement)
async def get_song_arrangement(
    song_id: int,  # noqa: ARG001
    arrangement_id: int,
    db: DbSessionDep,
):
    return get_song_arrangement_by_id(arrangement_id, db)


@song_router.post("/{song_id}/arrangements", response_model=SongArrangement, status_code=201)
async def create_song_arrangement_endpoint(
    song_id: int,  # noqa: ARG001
    data: SongArrangementCreate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return create_song_arrangement(data, current_user.id, db)


@song_router.put("/{song_id}/arrangements/{arrangement_id}", response_model=SongArrangement)
async def update_song_arrangement_endpoint(
    song_id: int,  # noqa: ARG001
    arrangement_id: int,
    data: SongArrangementUpdate,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return update_song_arrangement(arrangement_id, data, db)


@song_router.delete("/{song_id}/arrangements/{arrangement_id}", response_model=SongArrangement)
async def delete_song_arrangement_endpoint(
    song_id: int,  # noqa: ARG001
    arrangement_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return delete_song_arrangement(arrangement_id, db)
