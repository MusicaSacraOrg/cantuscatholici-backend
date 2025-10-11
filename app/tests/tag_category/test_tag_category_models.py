from app.tag_category.models import TagCategory


def test_create_tag_category(session):
    tag_category = TagCategory(name="Song Searching", color="#FF0000")
    session.add(tag_category)
    session.commit()

    assert tag_category.id is not None
    assert tag_category.name == "Song Searching"
    assert tag_category.color == "#FF0000"
    assert isinstance(tag_category.id, int)


def test_get_tag_category(session):
    tag_category = TagCategory(name="Song Searching", color="#00FF00")
    session.add(tag_category)
    session.commit()

    retrieved_tag_category = (
        session.query(TagCategory).filter_by(name="Song Searching").first()
    )
    assert retrieved_tag_category is not None
    assert retrieved_tag_category.name == "Song Searching"
    assert retrieved_tag_category.color == "#00FF00"
    assert isinstance(retrieved_tag_category.id, int)


def test_update_tag_category(session):
    tag_category = TagCategory(name="Song Searching", color="#0000FF")
    session.add(tag_category)
    session.commit()

    tag_category.name = "Song Part Searching"
    tag_category.color = "#FFFF00"
    session.commit()

    updated_tag_category = (
        session.query(TagCategory).filter_by(id=tag_category.id).first()
    )
    assert updated_tag_category.name == "Song Part Searching"
    assert updated_tag_category.color == "#FFFF00"


def test_delete_tag_category(session):
    tag_category = TagCategory(name="Song Searching", color="#FF00FF")
    session.add(tag_category)
    session.commit()

    session.delete(tag_category)
    session.commit()

    deleted_tag_category = (
        session.query(TagCategory).filter_by(id=tag_category.id).first()
    )
    assert deleted_tag_category is None
