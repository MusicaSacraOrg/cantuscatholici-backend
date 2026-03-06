from fastapi import status

from app.common.exceptions import DomainError


class TagNotFoundException(DomainError):
    code: str = "tag_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND


class TagNameTakenException(DomainError):
    code: str = "tag_name_taken"
    http_status: int = status.HTTP_409_CONFLICT
