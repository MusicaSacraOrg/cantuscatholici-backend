from fastapi import APIRouter, Query

from app.common.deps.pagination import PaginationParamsDep
from app.database import DbSessionDep
from app.song import service
from app.song.schema import SongDetail, SongListResponse

song_router = APIRouter(
    prefix="/song",
    tags=["Song"],
    responses={404: {"description": "Not found"}},
)


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
