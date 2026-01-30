import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user_role import UserRole


def test_create_user_role(session):
    user_role = UserRole(role="Admin")
    session.add(user_role)
    session.commit()

    assert user_role.id is not None
    assert user_role.role == "Admin"
    assert isinstance(user_role.id, int)


def test_get_user_role(session):
    user_role = UserRole(role="Admin")
    session.add(user_role)
    session.commit()

    retrieved_user_role = session.query(UserRole).filter_by(role="Admin").first()
    assert retrieved_user_role is not None
    assert retrieved_user_role.role == "Admin"
    assert isinstance(retrieved_user_role.id, int)


def test_update_user_role(session):
    user_role = UserRole(role="Admin")
    session.add(user_role)
    session.commit()

    user_role.role = "SuperAdmin"
    session.commit()

    updated_user_role = session.query(UserRole).filter_by(id=user_role.id).first()
    assert updated_user_role.role == "SuperAdmin"


def test_delete_user_role(session):
    user_role = UserRole(role="Admin")
    session.add(user_role)
    session.commit()

    session.delete(user_role)
    session.commit()

    deleted_user_role = session.query(UserRole).filter_by(id=user_role.id).first()
    assert deleted_user_role is None

def test_user_role_unique_constraint(session):
    user_role1 = UserRole(role="Admin")
    user_role2 = UserRole(role="Admin")

    session.add(user_role1)
    session.commit()

    session.add(user_role2)
    with pytest.raises(IntegrityError):
        session.commit()
