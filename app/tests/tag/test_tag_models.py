import pytest
from sqlalchemy.exc import IntegrityError

from app.tag.models import Tag


def test_dummy(
    testclient,
):
    response = testclient.get("/tag")
    assert response.status_code == 200


def test_create_tag(session):
    tag = Tag(name="Advent")
    session.add(tag)
    session.commit()

    assert tag.id is not None
    assert tag.name == "Advent"
    assert isinstance(tag.id, int)


def test_get_tag(session):
    tag = Tag(name="Advent")
    session.add(tag)
    session.commit()

    retrieved_tag = session.query(Tag).filter_by(name="Advent").first()
    assert retrieved_tag is not None
    assert retrieved_tag.name == "Advent"
    assert isinstance(retrieved_tag.id, int)


def test_update_tag(session):
    tag = Tag(name="Advent")
    session.add(tag)
    session.commit()

    tag.name = "Christmas"
    session.commit()

    updated_tag = session.query(Tag).filter_by(id=tag.id).first()
    assert updated_tag.name == "Christmas"


def test_delete_tag(session):
    tag = Tag(name="Advent")
    session.add(tag)
    session.commit()

    session.delete(tag)
    session.commit()

    deleted_tag = session.query(Tag).filter_by(id=tag.id).first()
    assert deleted_tag is None


def test_tag_unique_constraint(session):
    tag1 = Tag(name="Advent")
    tag2 = Tag(name="Advent")

    session.add(tag1)
    session.commit()

    session.add(tag2)
    with pytest.raises(IntegrityError):
        session.commit()
