from typing import ClassVar

from fastapi import status


class DomainError(Exception):
    code: str = "domain_error"
    http_status: int = status.HTTP_400_BAD_REQUEST
    headers: ClassVar[dict[str, str]] = {}

    def __init__(self, message: str, extra: dict | None = None):
        super().__init__(message)
        self.extra = extra or {}


class NotFoundError(DomainError):
    code: str = "not_found"
    http_status: int = status.HTTP_404_NOT_FOUND

    def __init__(self, entity: str, *, extra: dict | None = None):
        super().__init__(f"{entity} not found", extra=extra)


class AlreadyExistsError(DomainError):
    code: str = "already_exists"
    http_status: int = status.HTTP_409_CONFLICT

    def __init__(self, entity: str, *, extra: dict | None = None):
        super().__init__(f"{entity} already exists", extra=extra)