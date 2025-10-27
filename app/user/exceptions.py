from typing import ClassVar

from fastapi import status

from app.common.exceptions import DomainError


class EmailTakenException(DomainError):
    code: str = "email_taken"
    http_status: int = status.HTTP_409_CONFLICT


class MobileTakenException(DomainError):
    code: str = "mobile_taken"
    http_status: int = status.HTTP_409_CONFLICT


class InvalidCredentialsException(DomainError):
    code: str = "invalid_credentials"
    http_status: int = status.HTTP_401_UNAUTHORIZED
    headers: ClassVar[dict[str, str]] = {"WWW-Authenticate": "Bearer"}


class InvalidRefreshTokenException(DomainError):
    code: str = "invalid_refresh_token"
    http_status: int = status.HTTP_401_UNAUTHORIZED
    headers: ClassVar[dict[str, str]] = {"WWW-Authenticate": "Bearer"}
