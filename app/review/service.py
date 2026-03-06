from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.review.exceptions import ReviewNotFoundException
from app.review.models import ReviewComment
from app.song.models import SongMr


def list_reviews(
    session: Session, status_filter: str | None = None,
) -> list[dict]:
    stmt = select(SongMr).order_by(SongMr.id.desc())
    if status_filter:
        stmt = stmt.where(SongMr.status == status_filter)
    reviews = list(session.scalars(stmt).all())
    return [_review_to_dict(r) for r in reviews]


def get_review(session: Session, review_id: int) -> dict:
    review = session.get(SongMr, review_id)
    if review is None:
        raise ReviewNotFoundException("Review not found")

    comments = list(session.scalars(
        select(ReviewComment)
        .where(ReviewComment.review_id == review_id)
        .order_by(ReviewComment.created_at.asc())
    ).all())

    result = _review_to_dict(review)
    result["comments"] = [
        {
            "id": c.id,
            "commenter_id": c.commenter_id,
            "content": c.content,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in comments
    ]
    return result


def create_review(
    session: Session,
    reviewable_id: int,
    user_id: int,
    redactor_id: int,
) -> dict:
    review = SongMr(
        reviewable_id=reviewable_id,
        user_id=user_id,
        redactor_id=redactor_id,
        status="open",
    )
    session.add(review)
    session.commit()
    return _review_to_dict(review)


def approve_review(session: Session, review_id: int) -> dict:
    review = session.get(SongMr, review_id)
    if review is None:
        raise ReviewNotFoundException("Review not found")
    review.status = "approved"
    review.closed_at = datetime.now(timezone.utc)
    session.commit()
    return _review_to_dict(review)


def reject_review(session: Session, review_id: int) -> dict:
    review = session.get(SongMr, review_id)
    if review is None:
        raise ReviewNotFoundException("Review not found")
    review.status = "rejected"
    review.closed_at = datetime.now(timezone.utc)
    session.commit()
    return _review_to_dict(review)


def add_comment(
    session: Session,
    review_id: int,
    commenter_id: int,
    content: str,
) -> dict:
    review = session.get(SongMr, review_id)
    if review is None:
        raise ReviewNotFoundException("Review not found")

    comment = ReviewComment(
        review_id=review_id,
        commenter_id=commenter_id,
        content=content,
    )
    session.add(comment)
    session.commit()
    return {
        "id": comment.id,
        "review_id": review_id,
        "commenter_id": commenter_id,
        "content": content,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
    }


def _review_to_dict(review: SongMr) -> dict:
    return {
        "id": review.id,
        "reviewable_id": review.reviewable_id,
        "user_id": review.user_id,
        "redactor_id": review.redactor_id,
        "status": review.status,
        "closed_at": review.closed_at.isoformat() if review.closed_at else None,
    }
