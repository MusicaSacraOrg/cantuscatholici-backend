from fastapi import status

from app.common.exceptions import DomainError


class TagCategoryNotFoundException(DomainError):
    code: str = "tag_category_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND


class TagCategoryNameTakenException(DomainError):
    code: str = "tag_category_name_taken"
    http_status: int = status.HTTP_409_CONFLICT
