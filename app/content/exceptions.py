from fastapi import status

from app.common.exceptions import DomainError


class MsczContentNotFoundException(DomainError):
    code: str = "mscz_content_not_found"
    http_status: int = status.HTTP_404_NOT_FOUND
