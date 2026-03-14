from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import AlreadyExistsError, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.tag import (
    db_create_tag,
    db_delete_tag,
    db_get_tag_by_id,
    db_get_tags,
    db_get_tags_by_category,
    db_update_tag,
)
from app.models.tag import Tag
from app.schemas.tag import Tag as TagSchema
from app.schemas.tag import TagCreate as TagCreateSchema


def get_tags(db: Session, pagination: PaginationParams) -> Paginated[TagSchema]:
    total, items = db_get_tags(
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
    )

    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )

def get_tag_by_id(tag_id: int, db: Session) -> TagSchema:
    tag = db_get_tag_by_id(tag_id, db)

    if not tag:
        raise NotFoundError('Tag')

    return tag


def get_tags_by_category(
        tag_category_id: int,
        db: Session,
        pagination: PaginationParams,
) -> Paginated[TagSchema]:
    total, items = db_get_tags_by_category(
        tag_category_id,
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
    )
    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )


def create_tag(tag: TagCreateSchema, db: Session) -> TagSchema:
    new_tag = Tag(
        name=tag.name,
        tag_category_id=tag.tag_category_id,
    )

    try:
        return db_create_tag(new_tag, db)
    except IntegrityError as e:
        if 'unique' in str(e.orig).lower():
            raise AlreadyExistsError('Tag') from e
        raise


def update_tag(tag_id: int, tag: TagCreateSchema, db: Session) -> TagSchema:
    existing_tag = db_get_tag_by_id(tag_id, db)
    if existing_tag is None:
        raise NotFoundError('Tag') from None

    existing_tag.name = tag.name
    existing_tag.category_id = tag.category_id

    try:
        return db_update_tag(existing_tag, db)
    except IntegrityError as e:
        if 'unique' in str(e.orig).lower():
            raise AlreadyExistsError('Tag') from e
        raise


def delete_tag(tag_id: int, db: Session) -> TagSchema:
    existing_tag = db_get_tag_by_id(tag_id, db)
    if existing_tag is None:
        raise NotFoundError('Tag') from None

    return db_delete_tag(existing_tag, db)
