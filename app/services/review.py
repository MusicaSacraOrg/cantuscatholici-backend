from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import ForbiddenException, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.review import (
    db_create_review_comment,
    db_create_review_request,
    db_delete_review_comment,
    db_delete_review_request,
    db_get_comments_by_review,
    db_get_review_comment_by_id,
    db_get_review_request_by_id,
    db_get_review_requests,
    db_update_review_request,
)
from app.models.review import ReviewComment, ReviewRequest
from app.schemas.review import (
    ReviewComment as ReviewCommentSchema,
    ReviewCommentCreate,
    ReviewRequest as ReviewRequestSchema,
    ReviewRequestCreate,
    ReviewRequestUpdate,
)


def get_review_requests(
    db: Session,
    pagination: PaginationParams,
    *,
    open_only: bool = False,
) -> Paginated[ReviewRequestSchema]:
    total, items = db_get_review_requests(
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        open_only=open_only,
    )
    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )


def get_review_request_by_id(review_id: int, db: Session) -> ReviewRequestSchema:
    review = db_get_review_request_by_id(review_id, db)
    if not review:
        raise NotFoundError("ReviewRequest")
    return review


def create_review_request(
    data: ReviewRequestCreate,
    requester_id: int,
    db: Session,
) -> ReviewRequestSchema:
    review = ReviewRequest(
        description=data.description,
        requester_id=requester_id,
        new_entity_id=data.new_entity_id,
        original_id=data.original_id,
        created_at=datetime.now(UTC),
    )
    return db_create_review_request(review, db)


def update_review_request(
    review_id: int,
    data: ReviewRequestUpdate,
    requester_id: int,
    db: Session,
) -> ReviewRequestSchema:
    review = db_get_review_request_by_id(review_id, db)
    if not review:
        raise NotFoundError("ReviewRequest")
    if review.requester_id != requester_id:
        raise ForbiddenException()
    if review.closed_at is not None:
        from app.common.exceptions import DomainError
        raise DomainError("Review request is already closed")

    review.description = data.description
    return db_update_review_request(review, db)


def approve_review_request(
    review_id: int,
    editor_id: int,
    db: Session,
) -> ReviewRequestSchema:
    review = db_get_review_request_by_id(review_id, db)
    if not review:
        raise NotFoundError("ReviewRequest")
    if review.closed_at is not None:
        from app.common.exceptions import DomainError
        raise DomainError("Review request is already closed")

    review.editor_id = editor_id
    review.closed_at = datetime.now(UTC)
    return db_update_review_request(review, db)


def reject_review_request(
    review_id: int,
    editor_id: int,
    db: Session,
) -> ReviewRequestSchema:
    review = db_get_review_request_by_id(review_id, db)
    if not review:
        raise NotFoundError("ReviewRequest")
    if review.closed_at is not None:
        from app.common.exceptions import DomainError
        raise DomainError("Review request is already closed")

    review.editor_id = editor_id
    review.closed_at = datetime.now(UTC)
    return db_update_review_request(review, db)


def delete_review_request(review_id: int, db: Session) -> ReviewRequestSchema:
    review = db_get_review_request_by_id(review_id, db)
    if not review:
        raise NotFoundError("ReviewRequest")
    return db_delete_review_request(review, db)


# --- ReviewComment ---

def get_review_comments(review_id: int, db: Session) -> list[ReviewCommentSchema]:
    if not db_get_review_request_by_id(review_id, db):
        raise NotFoundError("ReviewRequest")
    return db_get_comments_by_review(review_id, db)


def create_review_comment(
    review_id: int,
    data: ReviewCommentCreate,
    created_by_user_id: int,
    db: Session,
) -> ReviewCommentSchema:
    if not db_get_review_request_by_id(review_id, db):
        raise NotFoundError("ReviewRequest")

    comment = ReviewComment(
        review_request_id=review_id,
        content=data.content,
        created_by_user_id=created_by_user_id,
        created_at=datetime.now(UTC),
    )
    return db_create_review_comment(comment, db)


def delete_review_comment(
    comment_id: int,
    current_user_id: int,
    is_editor: bool,
    db: Session,
) -> ReviewCommentSchema:
    comment = db_get_review_comment_by_id(comment_id, db)
    if not comment:
        raise NotFoundError("ReviewComment")
    if not is_editor and comment.created_by_user_id != current_user_id:
        raise ForbiddenException()
    return db_delete_review_comment(comment, db)

