from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import AlreadyExistsError, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.author import (
    db_create_author,
    db_delete_author,
    db_get_author_by_id,
    db_get_authors,
    db_update_author,
)
from app.models.author import Author
from app.models.content_base import ContentBase
from app.models.person import Person
from app.schemas.author import Author as AuthorSchema
from app.schemas.author import AuthorCreate, AuthorUpdate


def get_authors(db: Session, pagination: PaginationParams) -> Paginated[AuthorSchema]:
    total, items = db_get_authors(
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


def get_author_by_id(author_id: int, db: Session) -> AuthorSchema:
    author = db_get_author_by_id(author_id, db)
    if not author:
        raise NotFoundError("Author")
    return author


def create_author(data: AuthorCreate, added_by_user_id: int, db: Session) -> AuthorSchema:
    content_base = ContentBase()
    db.add(content_base)
    db.flush()

    person = Person(
        name=data.name,
        surname=data.surname,
        description=data.description,
        avatar_id=data.avatar_id,
    )
    db.add(person)
    db.flush()

    author = Author(
        id=person.id,
        content_base_id=content_base.id,
        added_by_user_id=added_by_user_id,
        added_at=datetime.now(UTC),
    )

    try:
        return db_create_author(author, db)
    except IntegrityError as e:
        db.rollback()
        raise AlreadyExistsError("Author") from e


def update_author(author_id: int, data: AuthorUpdate, db: Session) -> AuthorSchema:
    author = db_get_author_by_id(author_id, db)
    if not author:
        raise NotFoundError("Author")

    # Author inherits from Person, update person fields
    person = author.person
    person.name = data.name
    person.surname = data.surname
    person.description = data.description
    person.avatar_id = data.avatar_id

    return db_update_author(author, db)


def delete_author(author_id: int, db: Session) -> AuthorSchema:
    author = db_get_author_by_id(author_id, db)
    if not author:
        raise NotFoundError("Author")
    return db_delete_author(author, db)

