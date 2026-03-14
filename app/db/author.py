from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.author import Author

ALLOWED_ORDER_FIELDS = {
    "id": Author.id,
    "name": Author.name,
    "surname": Author.surname,
    "added_at": Author.added_at,
}


def db_get_authors(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[Author]]:
    total = db.execute(select(func.count()).select_from(Author)).scalar_one()

    stmt = select(Author)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_author_by_id(author_id: int, db: Session) -> Author | None:
    return db.execute(select(Author).where(Author.id == author_id)).scalars().first()


def db_create_author(author: Author, db: Session) -> Author:
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def db_update_author(author: Author, db: Session) -> Author:
    db.commit()
    db.refresh(author)
    return author


def db_delete_author(author: Author, db: Session) -> Author:
    db.delete(author)
    db.commit()
    return author

