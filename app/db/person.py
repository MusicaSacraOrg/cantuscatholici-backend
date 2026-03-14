from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.person import Person

ALLOWED_ORDER_FIELDS = {
    "id": Person.id,
    "name": Person.name,
    "surname": Person.surname,
}


def db_get_persons(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[Person]]:
    total = db.execute(select(func.count()).select_from(Person)).scalar_one()

    stmt = select(Person)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_person_by_id(person_id: int, db: Session) -> Person | None:
    return db.execute(select(Person).where(Person.id == person_id)).scalars().first()


def db_update_person(person: Person, db: Session) -> Person:
    db.commit()
    db.refresh(person)
    return person


def db_delete_person(person: Person, db: Session) -> Person:
    db.delete(person)
    db.commit()
    return person

