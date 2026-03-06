from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import AlreadyExistsError, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.tag_category import (
    db_create_tag_category,
    db_delete_tag_category,
    db_get_tag_category,
    db_get_tags_categories,
    db_update_tag_category,
)
from app.models.tag_category import TagCategory
from app.schemas.tag_category import TagCategory as TagCategorySchema
from app.schemas.tag_category import TagCategoryCreate as TagCategoryCreateSchema


def get_tag_categories(
    db: Session,
    pagination: PaginationParams,
) -> Paginated[TagCategorySchema]:
    total, items = db_get_tags_categories(
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


def get_tag_category_by_id(tag_category_id: int, db: Session) -> TagCategorySchema:
    tag = db_get_tag_category(tag_category_id, db)

    if not tag:
        raise NotFoundError("TagCategory")

    return tag


def create_tag_category(
    tag_category: TagCategoryCreateSchema,
    db: Session,
) -> TagCategorySchema:
    new_tag_category = TagCategory(
        name=tag_category.name,
    )

    try:
        return db_create_tag_category(new_tag_category, db)
    except IntegrityError as e:
        if "unique" in str(e.orig).lower():
            raise AlreadyExistsError("TagCategory") from e
        raise


def update_tag_category(
    tag_category_id: int, tag_category: TagCategoryCreateSchema, db: Session,
) -> TagCategorySchema:
    existing_tag_category = db_get_tag_category(tag_category_id, db)
    if existing_tag_category is None:
        raise NotFoundError("TagCategory") from None

    existing_tag_category.name = tag_category.name

    try:
        return db_update_tag_category(existing_tag_category, db)
    except IntegrityError as e:
        if "unique" in str(e.orig).lower():
            raise AlreadyExistsError("TagCategory") from e
        raise


def delete_tag_category(tag_category_id: int, db: Session) -> TagCategorySchema:
    existing_tag_category = db_get_tag_category(tag_category_id, db)
    if existing_tag_category is None:
        raise NotFoundError("TagCategory") from None

    return db_delete_tag_category(existing_tag_category, db)
