from fastapi import APIRouter
from pydantic import BaseModel

from app.database import DbSessionDep
from app.transposition import service

transposition_router = APIRouter(
    prefix="/song",
    tags=["Transposition"],
)


class TransposeRequest(BaseModel):
    semitones: int


@transposition_router.post("/{song_id}/transpose")
def transpose_song(
    session: DbSessionDep,
    song_id: int,
    body: TransposeRequest,
):
    return service.transpose_mscz(session, song_id, body.semitones)


@transposition_router.get("/{song_id}/transpositions")
def get_transpositions(session: DbSessionDep, song_id: int):
    return service.get_transpositions(session, song_id)
