from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.tag import Tag


def db_get_tags(db: Session) -> list[Tag]:
    result = db.execute(
        select(Tag)
    )
    return result.scalars().all()


def db_get_tag_by_id(tag_id: int, db: Session) -> Tag | None:
    result = db.execute(
        select(Tag).where(Tag.id == tag_id)
    )
    return result.scalars().first()


def db_get_tags_by_category(tag_category_id: int, db: Session) -> list[Tag] | None:
    result = db.execute(
        select(Tag).where(Tag.category_id == tag_category_id)
    )
    return result.scalars().all()


def db_create_tag(tag: Tag, db: Session) -> Tag:
    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def db_update_tag(tag: Tag, db: Session) -> Tag:
    db.commit()
    db.refresh(tag)

    return tag


def db_delete_tag(tag: Tag, db: Session) -> Tag:
    db.delete(tag)
    db.commit()

    return tag
