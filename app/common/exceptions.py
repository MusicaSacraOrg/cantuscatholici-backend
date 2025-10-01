from typing import ClassVar

from fastapi import status


class DomainError(Exception):
    code: str = "domain_error"
    http_status: int = status.HTTP_400_BAD_REQUEST
    headers: ClassVar[dict[str, str]] = {}

    def __init__(self, message: str, extra: dict | None = None):
        super().__init__(message)
        self.extra = extra or {}
