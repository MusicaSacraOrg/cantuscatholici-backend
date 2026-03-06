from fastapi import status

from app.common.exceptions import DomainError


class UserContentNotFoundException(DomainError):
    code: str = "user_content_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND


class UserContentForbiddenException(DomainError):
    code: str = "user_content_forbidden"
    http_status: int = status.HTTP_403_FORBIDDEN
