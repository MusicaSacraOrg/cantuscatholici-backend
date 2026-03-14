from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.celebration_category import CelebrationCategory

ALLOWED_ORDER_FIELDS = {
    "id": CelebrationCategory.id,
    "name": CelebrationCategory.name,
    "order_index": CelebrationCategory.order_index,
}


def db_get_celebration_categories(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[CelebrationCategory]]:
    total = db.execute(select(func.count()).select_from(CelebrationCategory)).scalar_one()

    stmt = select(CelebrationCategory)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_celebration_category_by_id(category_id: int, db: Session) -> CelebrationCategory | None:
    return (
        db.execute(select(CelebrationCategory).where(CelebrationCategory.id == category_id))
        .scalars()
        .first()
    )


def db_create_celebration_category(category: CelebrationCategory, db: Session) -> CelebrationCategory:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def db_update_celebration_category(category: CelebrationCategory, db: Session) -> CelebrationCategory:
    db.commit()
    db.refresh(category)
    return category


def db_delete_celebration_category(category: CelebrationCategory, db: Session) -> CelebrationCategory:
    db.delete(category)
    db.commit()
    return category

