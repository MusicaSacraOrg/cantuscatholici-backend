from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc

from ..models.tag import Tag

ALLOWED_ORDER_FIELDS = {
    "id": Tag.id,
    "name": Tag.name,
    "category_id": Tag.category_id,
}

def db_get_tags(db: Session, *, limit: int, offset: int, order_by: str | None = None, order: str = "asc",) -> tuple[int, list[Tag]]:
    total = db.execute(
        select(func.count()).select_from(Tag)
    ).scalar_one()

    stmt = select(Tag)

    if order_by in ALLOWED_ORDER_FIELDS:
        column = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

    if limit is not None:
        stmt = stmt.limit(limit)

    stmt = stmt.offset(offset)

    result = db.execute(stmt)
    items = result.scalars().all()

    return total, items


def db_get_tag_by_id(tag_id: int, db: Session,) -> Tag | None:
    result = db.execute(
        select(Tag).where(Tag.id == tag_id)
    )
    return result.scalars().first()


def db_get_tags_by_category(tag_category_id: int, db: Session,  *, limit: int, offset: int, order: str = "asc", order_by: str) -> tuple[int, list[Tag] | None]:
    total = db.execute(
        select(func.count()).select_from(Tag).where(Tag.category_id == tag_category_id)
    ).scalar_one()

    stmt = select(Tag).where(Tag.category_id == tag_category_id)

    if order_by in ALLOWED_ORDER_FIELDS:
        column = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

    if limit is not None:
        stmt = stmt.limit(limit)

    result = db.execute(stmt)
    items = result.scalars().all()

    return total, items


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
