from datetime import datetime

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.review import ReviewComment, ReviewRequest

ALLOWED_ORDER_FIELDS = {
    "id": ReviewRequest.id,
    "created_at": ReviewRequest.created_at,
    "closed_at": ReviewRequest.closed_at,
}


def db_get_review_requests(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
    open_only: bool = False,
) -> tuple[int, list[ReviewRequest]]:
    base_stmt = select(ReviewRequest)

    if open_only:
        base_stmt = base_stmt.where(ReviewRequest.closed_at.is_(None))

    total = db.execute(
        select(func.count()).select_from(base_stmt.subquery()),
    ).scalar_one()

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        base_stmt = base_stmt.order_by(asc(col) if order == "asc" else desc(col))

    base_stmt = base_stmt.limit(limit).offset(offset)
    items = list(db.execute(base_stmt).scalars().all())
    return total, items


def db_get_review_request_by_id(review_id: int, db: Session) -> ReviewRequest | None:
    return (
        db.execute(select(ReviewRequest).where(ReviewRequest.id == review_id))
        .scalars()
        .first()
    )


def db_create_review_request(review: ReviewRequest, db: Session) -> ReviewRequest:
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def db_update_review_request(review: ReviewRequest, db: Session) -> ReviewRequest:
    db.commit()
    db.refresh(review)
    return review


def db_delete_review_request(review: ReviewRequest, db: Session) -> ReviewRequest:
    db.delete(review)
    db.commit()
    return review


# --- ReviewComment ---

def db_get_comments_by_review(review_id: int, db: Session) -> list[ReviewComment]:
    return list(
        db.execute(
            select(ReviewComment)
            .where(ReviewComment.review_request_id == review_id)
            .order_by(ReviewComment.created_at),
        ).scalars().all(),
    )


def db_get_review_comment_by_id(comment_id: int, db: Session) -> ReviewComment | None:
    return (
        db.execute(select(ReviewComment).where(ReviewComment.id == comment_id))
        .scalars()
        .first()
    )


def db_create_review_comment(comment: ReviewComment, db: Session) -> ReviewComment:
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def db_delete_review_comment(comment: ReviewComment, db: Session) -> ReviewComment:
    db.delete(comment)
    db.commit()
    return comment

