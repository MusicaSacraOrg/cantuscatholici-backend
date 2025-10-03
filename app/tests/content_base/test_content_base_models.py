from app.content_base.models import ContentBase


def test_create_content_base(session):
    content_base = ContentBase()
    session.add(content_base)
    session.commit()

    assert content_base.id is not None
    assert content_base.type == "content_base"
    assert isinstance(content_base.id, int)


def test_get_content_base(session):
    content_base = ContentBase()
    session.add(content_base)
    session.commit()

    retrieved_content_base = session.query(ContentBase).filter_by().first()
    assert retrieved_content_base is not None
    assert isinstance(retrieved_content_base.id, int)


def test_delete_content_base(session):
    content_base = ContentBase()
    session.add(content_base)
    session.commit()

    session.delete(content_base)
    session.commit()

    deleted_content_base = (
        session.query(ContentBase).filter_by(id=content_base.id).first()
    )
    assert deleted_content_base is None
