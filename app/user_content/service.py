from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.review.service import create_review
from app.user.models import UserContent
from app.user_content.exceptions import (
    UserContentForbiddenException,
    UserContentNotFoundException,
)


def _uc_to_dict(uc: UserContent) -> dict:
    added_by_name = None
    if uc.added_by_user:
        u = uc.added_by_user
        added_by_name = f"{u.name} {u.surname}".strip()

    return {
        "id": uc.id,
        "title": uc.title,
        "description": uc.description,
        "content_type": uc.content_type,
        "file_id": uc.file_id,
        "mscz_id": uc.mscz_id,
        "author": uc.author,
        "added_by_user_id": uc.added_by_user_id,
        "added_by_name": added_by_name,
        "song_id": uc.song_id,
        "added_at": uc.added_at.isoformat() if uc.added_at else None,
    }


def get_song_user_content(session: Session, song_id: int) -> dict:
    stmt = (
        select(UserContent)
        .where(UserContent.song_id == song_id)
        .options(selectinload(UserContent.added_by_user))
        .order_by(UserContent.added_at.desc())
    )
    items = list(session.scalars(stmt).unique().all())
    count = session.scalar(
        select(func.count()).select_from(UserContent).where(
            UserContent.song_id == song_id
        )
    )
    return {
        "total": count or 0,
        "limit": 100,
        "offset": 0,
        "items": [_uc_to_dict(uc) for uc in items],
    }


def create_user_content(
    session: Session,
    song_id: int,
    user_id: int,
    title: str,
    description: str | None = None,
    content_type: str | None = None,
    file_id: int | None = None,
    mscz_id: int | None = None,
) -> dict:
    uc = UserContent(
        title=title,
        description=description,
        content_type=content_type,
        file_id=file_id,
        mscz_id=mscz_id,
        added_by_user_id=user_id,
        song_id=song_id,
    )
    session.add(uc)
    session.commit()

    # Auto-create review for moderation
    create_review(
        session,
        reviewable_id=uc.id,
        user_id=user_id,
        redactor_id=user_id,  # default to self, redactor can reassign
    )

    session.refresh(uc, attribute_names=["added_by_user"])
    return _uc_to_dict(uc)


def get_user_content(session: Session, uc_id: int) -> dict:
    uc = session.scalars(
        select(UserContent)
        .where(UserContent.id == uc_id)
        .options(selectinload(UserContent.added_by_user))
    ).first()
    if uc is None:
        raise UserContentNotFoundException("User content not found")
    return _uc_to_dict(uc)


def update_user_content(
    session: Session,
    uc_id: int,
    user_id: int,
    title: str,
    description: str | None = None,
    content_type: str | None = None,
) -> dict:
    uc = session.get(UserContent, uc_id)
    if uc is None:
        raise UserContentNotFoundException("User content not found")
    if uc.added_by_user_id != user_id:
        raise UserContentForbiddenException("Not your content")
    uc.title = title
    uc.description = description
    uc.content_type = content_type
    session.commit()
    session.refresh(uc, attribute_names=["added_by_user"])
    return _uc_to_dict(uc)


def delete_user_content(session: Session, uc_id: int, user_id: int) -> None:
    uc = session.get(UserContent, uc_id)
    if uc is None:
        raise UserContentNotFoundException("User content not found")
    if uc.added_by_user_id != user_id:
        raise UserContentForbiddenException("Not your content")
    session.delete(uc)
    session.commit()
