import pytest
from sqlalchemy.exc import IntegrityError

from app.tag.models import Tag
from app.tag_category.models import TagCategory


def test_create_tag_category(session):
    tag = Tag(name="Advent")
    session.add(tag)
    session.commit()

    tag_category = TagCategory(
        name="Song Searching", tag_id=tag.id, color="#FF0000")
    session.add(tag_category)
    session.commit()

    assert tag_category.id is not None
    assert tag_category.name == "Song Searching"
    assert tag_category.tag_id == tag.id
    assert tag_category.color == "#FF0000"
    assert isinstance(tag_category.id, int)


def test_get_tag_category(session):
    tag = Tag(name="Christmas")
    session.add(tag)
    session.commit()

    tag_category = TagCategory(
        name="Song Searching", tag_id=tag.id, color="#00FF00")
    session.add(tag_category)
    session.commit()

    retrieved_tag_category = session.query(
        TagCategory).filter_by(name="Song Searching").first()
    assert retrieved_tag_category is not None
    assert retrieved_tag_category.name == "Song Searching"
    assert retrieved_tag_category.tag_id == tag.id
    assert retrieved_tag_category.color == "#00FF00"
    assert isinstance(retrieved_tag_category.id, int)


def test_update_tag_category(session):
    tag = Tag(name="Lent")
    session.add(tag)
    session.commit()

    tag_category = TagCategory(
        name="Song Searching", tag_id=tag.id, color="#0000FF")
    session.add(tag_category)
    session.commit()

    tag_category.name = "Song Part Searching"
    tag_category.color = "#FFFF00"
    session.commit()

    updated_tag_category = session.query(
        TagCategory).filter_by(id=tag_category.id).first()
    assert updated_tag_category.name == "Song Part Searching"
    assert updated_tag_category.color == "#FFFF00"


def test_delete_tag_category(session):
    tag = Tag(name="Easter")
    session.add(tag)
    session.commit()

    tag_category = TagCategory(
        name="Song Searching", tag_id=tag.id, color="#FF00FF")
    session.add(tag_category)
    session.commit()

    session.delete(tag_category)
    session.commit()

    deleted_tag_category = session.query(
        TagCategory).filter_by(id=tag_category.id).first()
    assert deleted_tag_category is None


def test_tag_category_foreign_key_constraint(session):
    tag_category = TagCategory(
        name="Song Searching", tag_id=999, color="#000000")
    session.add(tag_category)

    with pytest.raises(IntegrityError):
        session.commit()


def test_tag_category_nullable_constraints(session):
    tag = Tag(name="Ordinary Time")
    session.add(tag)
    session.commit()

    tag_category = TagCategory(name=None, tag_id=tag.id, color="#FFFFFF")
    session.add(tag_category)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()

    tag_category = TagCategory(
        name="Song Searching", tag_id=None, color="#FFFFFF")
    session.add(tag_category)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()

    tag_category = TagCategory(
        name="Song Searching", tag_id=tag.id, color=None)
    session.add(tag_category)

    with pytest.raises(IntegrityError):
        session.commit()
