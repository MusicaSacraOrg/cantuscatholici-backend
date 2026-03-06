from fastapi import status

from app.common.exceptions import DomainError


class StaticContentNotFoundException(DomainError):
    code: str = "static_content_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND


class InvalidFileTypeException(DomainError):
    code: str = "invalid_file_type"
    http_status: int = status.HTTP_400_BAD_REQUEST


class FileTooLargeException(DomainError):
    code: str = "file_too_large"
    http_status: int = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
