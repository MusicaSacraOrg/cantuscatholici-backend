from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.person.exceptions import PersonNotFoundException
from app.person.models import Person


def get_persons(
    session: Session,
    pagination: PaginationParams,
) -> dict:
    total = session.scalar(select(func.count()).select_from(Person))
    items = session.scalars(
        select(Person).offset(pagination.offset).limit(pagination.limit),
    ).all()

    return {
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset,
        "items": items,
    }


def get_person(session: Session, person_id: int) -> Person:
    person = session.get(Person, person_id)
    if person is None:
        raise PersonNotFoundException("Person not found")
    return person


def create_person(
    session: Session,
    name: str,
    surname: str,
    description: str | None = None,
) -> Person:
    person = Person(name=name, surname=surname, description=description)
    with session.begin():
        session.add(person)
    session.refresh(person)
    return person
