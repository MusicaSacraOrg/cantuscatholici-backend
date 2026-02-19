from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc

from ..models.tag_category import TagCategory

ALLOWED_ORDER_FIELDS = {
    "id": TagCategory.id,
    "name": TagCategory.name,
}

def db_get_tags_categories(db: Session, *, limit: int, offset: int, order_by: str | None = None, order: str = "asc",) -> tuple[int, list[TagCategory]]:
    total = db.execute(
        select(func.count()).select_from(TagCategory)
    ).scalar_one()

    stmt = select(TagCategory)

    if order_by in ALLOWED_ORDER_FIELDS:
        column = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

    if limit is not None:
        stmt = stmt.limit(limit)

    stmt = stmt.offset(offset)

    result = db.execute(stmt)
    items = result.scalars().all()

    return total, items


def db_get_tag_category(tag_category_id: int, db: Session):
    result = db.execute(
        select(TagCategory).where(TagCategory.id == tag_category_id)
    )

    return result.scalars().first()


def db_create_tag_category(tag_category: TagCategory, db: Session):
    db.add(tag_category)
    db.commit()
    db.refresh(tag_category)

    return tag_category


def db_update_tag_category(tag_category: TagCategory, db: Session):
    db.commit()
    db.refresh(tag_category)

    return tag_category


def db_delete_tag_category(tag_category: TagCategory, db: Session):
    db.delete(tag_category)
    db.commit()

    return tag_category