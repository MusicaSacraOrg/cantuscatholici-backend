import pytest
from sqlalchemy.exc import IntegrityError

from app.static_content.models import StaticContent


def test_dummy(testclient):
    response = testclient.get("/static_content")
    assert response.status_code == 200


def test_create_static_content(session):
    static_content = StaticContent(path="/images/avatar.jpg")
    session.add(static_content)
    session.commit()

    assert static_content.id is not None
    assert static_content.path == "/images/avatar.jpg"
    assert static_content.type == "static_content"
    assert isinstance(static_content.id, int)


def test_get_static_content(session):
    static_content = StaticContent(path="/images/avatar.jpg")
    session.add(static_content)
    session.commit()

    retrieved_content = session.query(StaticContent).filter_by(
        path="/images/avatar.jpg").first()
    assert retrieved_content is not None
    assert retrieved_content.path == "/images/avatar.jpg"
    assert isinstance(retrieved_content.id, int)


def test_update_static_content(session):
    static_content = StaticContent(path="/images/avatar.jpg")
    session.add(static_content)
    session.commit()

    static_content.path = "/images/new_avatar.jpg"
    session.commit()

    updated_content = session.query(StaticContent).filter_by(
        id=static_content.id).first()
    assert updated_content.path == "/images/new_avatar.jpg"


def test_delete_static_content(session):
    static_content = StaticContent(path="/images/avatar.jpg")
    session.add(static_content)
    session.commit()

    session.delete(static_content)
    session.commit()

    deleted_content = session.query(StaticContent).filter_by(
        id=static_content.id).first()
    assert deleted_content is None


def test_static_content_unique_path_constraint(session):
    static_content1 = StaticContent(path="/images/avatar.jpg")
    static_content2 = StaticContent(path="/images/avatar.jpg")

    session.add(static_content1)
    session.commit()

    session.add(static_content2)
    with pytest.raises(IntegrityError):
        session.commit()
