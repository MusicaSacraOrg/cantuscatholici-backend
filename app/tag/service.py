from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.tag.exceptions import TagNameTakenException, TagNotFoundException
from app.tag.models import Tag


def get_tags(
    session: Session,
    pagination: PaginationParams,
    category_id: int | None = None,
) -> dict:
    base = select(Tag)
    count_base = select(func.count()).select_from(Tag)

    if category_id is not None:
        base = base.where(Tag.category_id == category_id)
        count_base = count_base.where(Tag.category_id == category_id)

    total = session.scalar(count_base)
    items = session.scalars(
        base.offset(pagination.offset).limit(pagination.limit),
    ).all()

    return {
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset,
        "items": items,
    }


def get_tag(session: Session, tag_id: int) -> Tag:
    tag = session.get(Tag, tag_id)
    if tag is None:
        raise TagNotFoundException("Tag not found")
    return tag


def create_tag(session: Session, name: str, category_id: int) -> Tag:
    tag = Tag(name=name, category_id=category_id)
    try:
        with session.begin():
            session.add(tag)
        session.refresh(tag)
    except IntegrityError as e:
        raise TagNameTakenException("Tag name already exists") from e
    return tag


def update_tag(
    session: Session,
    tag_id: int,
    name: str,
    category_id: int,
) -> Tag:
    tag = get_tag(session, tag_id)
    tag.name = name
    tag.category_id = category_id
    try:
        with session.begin():
            session.add(tag)
        session.refresh(tag)
    except IntegrityError as e:
        raise TagNameTakenException("Tag name already exists") from e
    return tag


def delete_tag(session: Session, tag_id: int) -> None:
    tag = get_tag(session, tag_id)
    with session.begin():
        session.delete(tag)
