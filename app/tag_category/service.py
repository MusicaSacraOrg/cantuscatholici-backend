from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.common.deps.pagination import PaginationParams
from app.tag_category.exceptions import (
    TagCategoryNameTakenException,
    TagCategoryNotFoundException,
)
from app.tag_category.models import TagCategory


def get_all_with_tags(session: Session) -> list[TagCategory]:
    stmt = select(TagCategory).options(selectinload(TagCategory.tags))
    return list(session.scalars(stmt).all())


def get_tag_categories(session: Session, pagination: PaginationParams) -> dict:
    total = session.scalar(select(func.count()).select_from(TagCategory))
    stmt = select(TagCategory).offset(pagination.offset).limit(pagination.limit)
    items = session.scalars(stmt).all()
    return {
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset,
        "items": items,
    }


def get_tag_category(session: Session, category_id: int) -> TagCategory:
    category = session.get(TagCategory, category_id)
    if category is None:
        raise TagCategoryNotFoundException("Tag category not found")
    return category


def create_tag_category(session: Session, name: str, color: str) -> TagCategory:
    category = TagCategory(name=name, color=color)
    try:
        with session.begin():
            session.add(category)
        session.refresh(category)
    except IntegrityError as e:
        raise TagCategoryNameTakenException("Tag category name already exists") from e
    return category


def update_tag_category(
    session: Session,
    category_id: int,
    name: str,
    color: str,
) -> TagCategory:
    category = get_tag_category(session, category_id)
    category.name = name
    category.color = color
    try:
        with session.begin():
            session.add(category)
        session.refresh(category)
    except IntegrityError as e:
        raise TagCategoryNameTakenException("Tag category name already exists") from e
    return category


def delete_tag_category(session: Session, category_id: int) -> None:
    category = get_tag_category(session, category_id)
    with session.begin():
        session.delete(category)
