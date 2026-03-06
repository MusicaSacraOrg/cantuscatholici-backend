from fastapi import status

from app.common.exceptions import DomainError


class SongNotFoundException(DomainError):
    code: str = "song_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND


class SongTitleTakenException(DomainError):
    code: str = "song_title_taken"
    http_status: int = status.HTTP_409_CONFLICT
