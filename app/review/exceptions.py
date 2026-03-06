from fastapi import status

from app.common.exceptions import DomainError


class ReviewNotFoundException(DomainError):
    code: str = "review_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND
