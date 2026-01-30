from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.tag import (
    db_get_tags,
    db_get_tag_by_id,
    db_create_tag,
    db_update_tag,
    db_delete_tag,
    db_get_tags_by_category,
)
from app.models.tag import Tag
from app.schemas.tag import Tag as TagSchema
from app.schemas.tag import TagCreate as TagCreateSchema


def get_tags(db: Session) -> list[Tag]:
    return db_get_tags(db)


def get_tag_by_id(tag_id: int, db: Session) -> Tag:
    tag = db_get_tag_by_id(tag_id, db)

    if not tag:
        # TODO error
        pass

    return tag


def get_tags_by_category(tag_category_id: int, db: Session) -> list[Tag]:
    return db_get_tags_by_category(tag_category_id, db)


def create_tag(tag: TagCreateSchema, db: Session) -> Tag:
    new_tag = Tag(
        name=tag.name,
        category_id=tag.category_id,
    )

    try:
        return db_create_tag(new_tag, db)
    except IntegrityError as e:
        if 'unique constraint' in str(e.orig).lower():
            # TODO error
            pass
        raise


def update_tag(tag_id: int, tag: TagCreateSchema, db: Session) -> Tag:
    existing_tag = db_get_tag_by_id(tag_id, db)
    if tag is None:
        # TODO error
        pass

    existing_tag.name = tag.name
    existing_tag.category_id = tag.category_id

    try:
        return db_update_tag(existing_tag, db)
    except IntegrityError as e:
        if 'unique constraint' in str(e.orig).lower():
            # TODO error
            pass
        raise


def delete_tag(tag_id: int, db: Session) -> Tag:
    existing_tag = db_get_tag_by_id(tag_id, db)
    if existing_tag is None:
        # TODO error
        pass

    return db_delete_tag(existing_tag, db)