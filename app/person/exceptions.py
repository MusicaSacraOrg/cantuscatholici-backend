from fastapi import status

from app.common.exceptions import DomainError


class PersonNotFoundException(DomainError):
    code: str = "person_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND
