from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.person import (
    db_delete_person,
    db_get_person_by_id,
    db_get_persons,
    db_update_person,
)
from app.schemas.person import PersonInDb, PersonUpdate


def get_persons(db: Session, pagination: PaginationParams) -> Paginated[PersonInDb]:
    total, items = db_get_persons(
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


def get_person_by_id(person_id: int, db: Session) -> PersonInDb:
    person = db_get_person_by_id(person_id, db)
    if not person:
        raise NotFoundError("Person")
    return person


def update_person(person_id: int, data: PersonUpdate, db: Session) -> PersonInDb:
    person = db_get_person_by_id(person_id, db)
    if not person:
        raise NotFoundError("Person")

    person.name = data.name
    person.surname = data.surname
    person.description = data.description
    person.avatar_id = data.avatar_id

    return db_update_person(person, db)


def delete_person(person_id: int, db: Session) -> PersonInDb:
    person = db_get_person_by_id(person_id, db)
    if not person:
        raise NotFoundError("Person")
    return db_delete_person(person, db)

