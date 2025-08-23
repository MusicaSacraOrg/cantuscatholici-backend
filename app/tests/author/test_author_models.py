from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.author.models import Author
from app.user.models import User
from app.user_role.models import UserRole


def test_create_author(session):
    role = UserRole(role="Admin")
    session.add(role)
    session.flush()

    user = User(
        name="Admin",
        surname="User",
        email="admin@example.com",
        role_id=role.id,
    )
    session.add(user)
    session.flush()

    author = Author(
        name="Create",
        surname="Author",
        added_by_user_id=user.id,
    )
    session.add(author)
    session.flush()
    session.commit()

    assert user.name == "Admin"
    assert user.surname == "User"
    assert author.id is not None
    assert author.name is not None
    assert author.surname is not None
    assert author.added_by_user_id == user.id
    assert isinstance(author.added_at, datetime)


def test_create_author_without_added_by_user(session):
    author = Author(name="Create", surname="Without")
    session.add(author)
    session.commit()

    assert author.id is not None
    assert author.name is not None
    assert author.surname is not None
    assert author.added_by_user_id is None
    assert isinstance(author.added_at, datetime)


def test_get_author(session):
    author = Author(name="Fetch", surname="Author")
    session.add(author)
    session.commit()

    found = session.query(Author).filter_by(name=author.name).first()
    assert found is not None
    assert found.id == author.id


def test_author_invalid_added_by_user_id(session):
    author = Author(added_by_user_id=999999)
    session.add(author)

    with pytest.raises(IntegrityError):
        session.commit()


def test_update_author(session):
    role = UserRole(role="User")
    session.add(role)
    session.flush()

    user1 = User(
        name="User1",
        surname="Smith",
        email="user1@example.com",
        role_id=role.id,
    )
    user2 = User(
        name="User2",
        surname="Jones",
        email="user2@example.com",
        role_id=role.id,
    )
    session.add_all([user1, user2])
    session.commit()

    author = Author(name="Update", surname="Author", added_by_user_id=user1.id)
    session.add(author)
    session.flush()
    session.commit()

    author.added_by_user_id = user2.id
    author.name = user2.name
    session.commit()

    updated = session.query(Author).filter_by(id=author.id).first()
    assert updated.added_by_user_id == user2.id
    assert updated.name == user2.name


def test_delete_author(session):
    author = Author(name="Delete", surname="Author")
    session.add(author)
    session.commit()

    session.delete(author)
    session.commit()

    deleted = session.query(Author).filter_by(id=author.id).first()
    assert deleted is None
