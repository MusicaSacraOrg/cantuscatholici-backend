from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database import DbSessionDep
from app.transposition import service
from app.user.schema import UserInDb
from app.user.service import get_current_user

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
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.transpose_mscz(session, song_id, body.semitones)


@transposition_router.get("/{song_id}/transpositions")
def get_transpositions(session: DbSessionDep, song_id: int):
    return service.get_transpositions(session, song_id)
