import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.tag.models import Tag
from app.tag_category.models import TagCategory


def test_dummy(
    testclient,
):
    response = testclient.get("/tag")
    assert response.status_code == 200


@pytest.fixture(scope="function")
def tag_category(session: Session):
    category = TagCategory(
        name="Test Category",
        color="#FF0000",
    )
    session.add(category)
    session.commit()
    session.refresh(category)

    yield category

    session.delete(category)
    session.commit()


@pytest.fixture(scope="function")
def tag(session: Session, tag_category: TagCategory):
    tag = Tag(name="Advent", category_id=tag_category.id)
    session.add(tag)
    session.commit()
    session.refresh(tag)

    assert tag.id is not None
    assert tag.name == "Advent"
    assert isinstance(tag.id, int)

    yield tag

    session.delete(tag)
    session.commit()


def test_create_tag(session, tag_category):
    tag = Tag(name="Advent", category_id=tag_category.id)
    session.add(tag)
    session.commit()

    assert tag.id is not None
    assert tag.name == "Advent"
    assert isinstance(tag.id, int)

    session.delete(tag)
    session.commit()


def test_get_tag(session, tag):
    retrieved_tag = session.query(Tag).filter_by(name=tag.name).first()
    assert retrieved_tag is not None
    assert retrieved_tag.name == "Advent"
    assert isinstance(retrieved_tag.id, int)
    retrieved_tag = None


def test_update_tag(session, tag):
    tag.name = "Christmas"
    session.commit()

    updated_tag = session.query(Tag).filter_by(id=tag.id).first()
    assert updated_tag.name == "Christmas"


def test_delete_tag(session, tag_category):
    tag = Tag(name="Advent", category_id=tag_category.id)
    session.add(tag)
    session.commit()

    session.delete(tag)
    session.commit()

    deleted_tag = session.query(Tag).filter_by(id=tag.id).first()
    assert deleted_tag is None


def test_tag_unique_constraint(session, tag_category):
    tag1 = Tag(name="Advent", category_id=tag_category.id)
    tag2 = Tag(name="Advent", category_id=tag_category.id)

    session.add(tag1)
    session.commit()

    session.add(tag2)
    with pytest.raises(IntegrityError):
        try:
            session.commit()
        finally:
            session.rollback()

    session.delete(tag1)
    session.commit()
