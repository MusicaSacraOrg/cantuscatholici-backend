from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.permissions import required_role
from app.common.deps.pagination import PaginationParamsDep
from app.common.schemas.pagination import Paginated
from app.database import DbSessionDep
from app.schemas.review import (
    ReviewComment,
    ReviewCommentCreate,
    ReviewRequest,
    ReviewRequestCreate,
    ReviewRequestUpdate,
)
from app.schemas.user import UserInDb
from app.services.review import (
    approve_review_request,
    create_review_comment,
    create_review_request,
    delete_review_comment,
    delete_review_request,
    get_review_comments,
    get_review_request_by_id,
    get_review_requests,
    reject_review_request,
    update_review_request,
)

review_router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
    responses={404: {"description": "Not found"}},
)


@review_router.get("/", response_model=Paginated[ReviewRequest])
async def list_reviews(
    db: DbSessionDep,
    pagination: PaginationParamsDep,
    open_only: bool = False,
    _user: UserInDb = Depends(required_role("Redactor")),  # noqa: B008
):
    return get_review_requests(db, pagination, open_only=open_only)


@review_router.get("/{review_id}", response_model=ReviewRequest)
async def get_review(
    review_id: int,
    db: DbSessionDep,
    _user: UserInDb = Depends(required_role("User")),  # noqa: B008
):
    return get_review_request_by_id(review_id, db)


@review_router.post("/", response_model=ReviewRequest, status_code=201)
async def create_review_endpoint(
    data: ReviewRequestCreate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return create_review_request(data, current_user.id, db)


@review_router.put("/{review_id}", response_model=ReviewRequest)
async def update_review_endpoint(
    review_id: int,
    data: ReviewRequestUpdate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return update_review_request(review_id, data, current_user.id, db)


@review_router.post("/{review_id}/approve", response_model=ReviewRequest)
async def approve_review_endpoint(
    review_id: int,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return approve_review_request(review_id, current_user.id, db)


@review_router.post("/{review_id}/reject", response_model=ReviewRequest)
async def reject_review_endpoint(
    review_id: int,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("Redactor"))],
):
    return reject_review_request(review_id, current_user.id, db)


@review_router.delete("/{review_id}", response_model=ReviewRequest)
async def delete_review_endpoint(
    review_id: int,
    db: DbSessionDep,
    _user: Annotated[UserInDb, Depends(required_role("Admin"))],
):
    return delete_review_request(review_id, db)


# --- Comments ---

@review_router.get("/{review_id}/comments", response_model=list[ReviewComment])
async def list_review_comments(
    review_id: int,
    db: DbSessionDep,
    _user: UserInDb = Depends(required_role("User")),  # noqa: B008
):
    return get_review_comments(review_id, db)


@review_router.post("/{review_id}/comments", response_model=ReviewComment, status_code=201)
async def create_review_comment_endpoint(
    review_id: int,
    data: ReviewCommentCreate,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    return create_review_comment(review_id, data, current_user.id, db)


@review_router.delete("/{review_id}/comments/{comment_id}", response_model=ReviewComment)
async def delete_review_comment_endpoint(
    review_id: int,  # noqa: ARG001
    comment_id: int,
    db: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(required_role("User"))],
):
    from app.services.user_role import PredefinedUserRoles

    is_editor = current_user.role in (PredefinedUserRoles.REDACTOR, PredefinedUserRoles.ADMIN)
    return delete_review_comment(comment_id, current_user.id, is_editor, db)
