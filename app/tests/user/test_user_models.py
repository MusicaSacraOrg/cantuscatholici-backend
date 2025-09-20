from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.user.models import User
from app.user_role.models import UserRole


def test_create_user(session):
    role = UserRole(role="Admin")
    session.add(role)
    session.commit()

    user = User(
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        mobile="1234567890",
        hashed_password="hashed_password",
        role_id=role.id,
    )
    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.email == "john.doe@example.com"
    assert user.mobile == "1234567890"
    assert user.role_id == role.id
    assert isinstance(user.registered_at, datetime)


def test_create_user_without_optional_mobile(session):
    role = UserRole(role="User")
    session.add(role)
    session.commit()

    user = User(
        name="Jane",
        surname="Doe",
        email="jane.doe@example.com",
        mobile=None,
        hashed_password="hashed_password",
        role_id=role.id,
    )
    session.add(user)
    session.commit()

    assert user.mobile is None


def test_create_user_missing_required_fields(session):
    user = User()
    session.add(user)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_user_email_must_be_unique(session):
    role = UserRole(role="TestRole")
    session.add(role)
    session.commit()

    user1 = User(
        name="Alpha",
        surname="Tester",
        email="duplicate@example.com",
        mobile="1111111111",
        hashed_password="hashed_password",
        role_id=role.id,
    )
    user2 = User(
        name="Beta",
        surname="Tester",
        email="duplicate@example.com",
        mobile="2222222222",
        role_id=role.id,
    )

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_user_mobile_must_be_unique_if_set(session):
    role = UserRole(role="AnotherRole")
    session.add(role)
    session.commit()

    user1 = User(
        name="Charlie",
        surname="Smith",
        email="charlie@example.com",
        mobile="9999999999",
        hashed_password="hashed_password",
        role_id=role.id,
    )
    user2 = User(
        name="Delta",
        surname="Smith",
        email="delta@example.com",
        mobile="9999999999",
        hashed_password="hashed_password",
        role_id=role.id,
    )

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()
