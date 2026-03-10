from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.common.deps.auth import require_role
from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.song import service
from app.song.schema import (
    LyricsUpdate,
    SongCreate,
    SongDetail,
    SongListResponse,
    SongLyrics,
    SongUpdate,
)
from app.user.schema import UserInDb
from app.user_role.service import PredefinedUserRoles

song_router = APIRouter(
    prefix="/song",
    tags=["Song"],
    responses={404: {"description": "Not found"}},
)

_require_redactor = require_role(PredefinedUserRoles.REDACTOR, PredefinedUserRoles.ADMIN)


@song_router.get("/", response_model=SongListResponse)
def get_songs(
    session: DbSessionDep,
    p: PaginationParamsDep,
    tags: str | None = Query(default=None, description="Comma-separated tag IDs"),
    search: str | None = Query(default=None),
    sort: str | None = Query(default=None),
    direction: str | None = Query(default=None),
):
    tag_ids = None
    if tags:
        tag_ids = [int(t) for t in tags.split(",") if t.strip().isdigit()]

    return service.get_songs(
        session,
        p,
        tag_ids=tag_ids,
        search_query=search,
        sort_by=sort,
        sort_dir=direction,
    )


@song_router.get("/{song_id}", response_model=SongDetail)
def get_song(session: DbSessionDep, song_id: int):
    return service.get_song_detail(session, song_id)


@song_router.post("/", response_model=SongDetail)
def create_song(
    session: DbSessionDep,
    body: SongCreate,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.create_song(
        session, body.title, body.author_id, body.description, body.tag_ids,
    )


@song_router.put("/{song_id}", response_model=SongDetail)
def update_song(
    session: DbSessionDep,
    song_id: int,
    body: SongUpdate,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.update_song(
        session, song_id, body.title, body.author_id, body.description, body.tag_ids,
    )


@song_router.delete("/{song_id}", status_code=204)
def delete_song(
    session: DbSessionDep,
    song_id: int,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    service.delete_song(session, song_id)


@song_router.get("/{song_id}/lyrics", response_model=SongLyrics)
def get_song_lyrics(session: DbSessionDep, song_id: int):
    return service.get_song_lyrics(session, song_id)


@song_router.put("/{song_id}/lyrics", response_model=SongLyrics)
def set_song_lyrics(
    session: DbSessionDep,
    song_id: int,
    body: LyricsUpdate,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    parts = [{"part_type": p.part_type, "lyrics": p.lyrics} for p in body.parts]
    return service.set_song_lyrics(session, song_id, parts)


class MsczAssociation(BaseModel):
    mscz_id: int


@song_router.put("/{song_id}/mscz", response_model=SongDetail)
def set_song_mscz(
    session: DbSessionDep,
    song_id: int,
    body: MsczAssociation,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.set_song_mscz(session, song_id, body.mscz_id)
