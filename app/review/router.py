from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.common.deps.auth import require_role
from app.database import DbSessionDep
from app.review import service
from app.user.schema import UserInDb
from app.user.service import get_current_user
from app.user_role.service import PredefinedUserRoles

review_router = APIRouter(
    prefix="/review",
    tags=["Review"],
    responses={404: {"description": "Not found"}},
)


class CommentBody(BaseModel):
    content: str


@review_router.get("/")
def list_reviews(
    session: DbSessionDep,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
    status: str | None = Query(default=None),
):
    return service.list_reviews(session, status_filter=status)


@review_router.get("/{review_id}")
def get_review(
    session: DbSessionDep,
    review_id: int,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.get_review(session, review_id)


_require_redactor = require_role(PredefinedUserRoles.REDACTOR, PredefinedUserRoles.ADMIN)


@review_router.post("/{review_id}/approve")
def approve_review(
    session: DbSessionDep,
    review_id: int,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.approve_review(session, review_id)


@review_router.post("/{review_id}/reject")
def reject_review(
    session: DbSessionDep,
    review_id: int,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.reject_review(session, review_id)


@review_router.post("/{review_id}/comment")
def add_comment(
    session: DbSessionDep,
    review_id: int,
    body: CommentBody,
    current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.add_comment(session, review_id, current_user.id, body.content)
