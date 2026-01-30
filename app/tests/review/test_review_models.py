from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.review import ReviewComment
from app.models.user import User
from app.models.user_role import UserRole


def test_create_review_comment(session):
    role = UserRole(role="User")
    session.add(role)
    session.flush()

    user = User(
        name="Test",
        surname="User",
        email="test@example.com",
        role_id=role.id,
        hashed_password="hashed_password",
    )
    session.add(user)
    session.commit()

    comment = ReviewComment(commenter_id=user.id, content="This is a comment.")
    session.add(comment)
    session.commit()

    assert comment.id is not None
    assert comment.commenter_id == user.id
    assert comment.content == "This is a comment."
    assert isinstance(comment.created_at, datetime)


def test_review_comment_required_fields(session):
    comment = ReviewComment(commenter_id=None, content="Missing user.")
    session.add(comment)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    role = UserRole(role="User")
    session.add(role)
    session.flush()

    user = User(
        name="John",
        surname="Doe",
        email="john@example.com",
        role_id=role.id,
        hashed_password="hashed_password",
    )
    session.add(user)
    session.commit()

    comment = ReviewComment(commenter_id=user.id, content=None)
    session.add(comment)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_review_comment_timestamp_default(session):
    role = UserRole(role="User")
    session.add(role)
    session.flush()

    user = User(
        name="Alice",
        surname="Smith",
        email="alice@example.com",
        role_id=role.id,
        hashed_password="hashed_password",
    )
    session.add(user)
    session.commit()

    comment = ReviewComment(commenter_id=user.id, content="With timestamp.")
    session.add(comment)
    session.commit()

    assert comment.created_at is not None
    assert isinstance(comment.created_at, datetime)


def test_delete_review_comment(session):
    role = UserRole(role="User")
    session.add(role)
    session.flush()

    user = User(
        name="Bob",
        surname="Doe",
        email="bob@example.com",
        role_id=role.id,
        hashed_password="hashed_password",
    )
    session.add(user)
    session.commit()

    comment = ReviewComment(commenter_id=user.id, content="To be deleted.")
    session.add(comment)
    session.commit()

    session.delete(comment)
    session.commit()

    deleted = session.query(ReviewComment).filter_by(id=comment.id).first()
    assert deleted is None


def test_dummy(
    testclient,
):
    response = testclient.get("/review")
    assert response.status_code == 200
