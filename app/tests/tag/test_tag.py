
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

    session.refresh(tag)

    assert tag.id is not None
    assert tag.name == "Advent"
    assert isinstance(tag.id, int)
