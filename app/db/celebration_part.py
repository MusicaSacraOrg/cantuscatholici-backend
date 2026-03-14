from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.celebration_part import CelebrationPart

ALLOWED_ORDER_FIELDS = {
    "id": CelebrationPart.id,
    "name": CelebrationPart.name,
    "order_index": CelebrationPart.order_index,
}


def db_get_celebration_parts(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[CelebrationPart]]:
    total = db.execute(select(func.count()).select_from(CelebrationPart)).scalar_one()

    stmt = select(CelebrationPart)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_celebration_part_by_id(part_id: int, db: Session) -> CelebrationPart | None:
    return (
        db.execute(select(CelebrationPart).where(CelebrationPart.id == part_id))
        .scalars()
        .first()
    )


def db_create_celebration_part(part: CelebrationPart, db: Session) -> CelebrationPart:
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


def db_update_celebration_part(part: CelebrationPart, db: Session) -> CelebrationPart:
    db.commit()
    db.refresh(part)
    return part


def db_delete_celebration_part(part: CelebrationPart, db: Session) -> CelebrationPart:
    db.delete(part)
    db.commit()
    return part

