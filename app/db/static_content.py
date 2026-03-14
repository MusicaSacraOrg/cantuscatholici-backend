from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.static_content import StaticContent

ALLOWED_ORDER_FIELDS = {
    "id": StaticContent.id,
    "path": StaticContent.path,
}


def db_get_static_contents(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[StaticContent]]:
    total = db.execute(select(func.count()).select_from(StaticContent)).scalar_one()

    stmt = select(StaticContent)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_static_content_by_id(static_content_id: int, db: Session) -> StaticContent | None:
    return (
        db.execute(select(StaticContent).where(StaticContent.id == static_content_id))
        .scalars()
        .first()
    )


def db_create_static_content(static_content: StaticContent, db: Session) -> StaticContent:
    db.add(static_content)
    db.commit()
    db.refresh(static_content)
    return static_content


def db_delete_static_content(static_content: StaticContent, db: Session) -> StaticContent:
    db.delete(static_content)
    db.commit()
    return static_content

