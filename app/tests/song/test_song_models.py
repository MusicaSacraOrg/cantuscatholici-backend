from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.content.models import MsczContent
from app.content_base.models import ContentBase
from app.person.models import Person
from app.song.models import Song, SongOrder, SongPart
from app.static_content.models import StaticContent
from app.tag.models import Tag
from app.user.models import User, UserContent
from app.user_role.models import UserRole


@pytest.fixture
def setup_related_entities(session):
    static = StaticContent(path="dummy/path", type="static_content")
    session.add(static)
    session.flush()

    role = UserRole(role="Admin")
    session.add(role)
    session.flush()

    author = Person(name="John", surname="Doe")
    session.add(author)
    session.flush()

    tag = Tag(name="Worship")
    session.add(tag)
    session.flush()

    song_part = SongPart(tag_id=tag.id)
    session.add(song_part)
    session.flush()

    song_order = SongOrder(order=1, part_id=song_part.id)
    session.add(song_order)
    session.flush()

    user = User(
        name="Uploader",
        surname="User",
        email="uploader@example.com",
        role_id=role.id,
        hashed_password="hashed_password",
    )
    session.add(user)
    session.flush()

    user_content = UserContent(
        title="User Upload",
        file_id=static.id,
        mscz_id=None,
        added_by_user_id=user.id,
        type="user_content",
    )
    session.add(user_content)
    session.flush()

    base_content = ContentBase()
    session.add(base_content)
    session.flush()

    mscz = MsczContent(
        c_mscz_file_id=static.id,
        c_svg_file_id=static.id,
        pdf_file_id=static.id,
        mp3_file_id=static.id,
    )
    session.add(mscz)
    session.commit()

    return {
        "author": author,
        "user": user,
        "tag": tag,
        "song_part": song_part,
        "song_order": song_order,
        "mscz": mscz,
        "user_content": user_content,
    }


def test_create_song(session, setup_related_entities):
    e = setup_related_entities

    song = Song(
        title="Amazing Grace",
        author=e["author"].id,
        description="A classic hymn.",
        added_by_user_id=e["user"].id,
        search_tag_id=e["tag"].id,
        song_part_id=e["song_part"].id,
        song_order_id=e["song_order"].id,
        mscz_id=e["mscz"].id,
        user_content_id=e["user_content"].id,
        related_id=None,
        lang_tag_id=e["tag"].id,
    )
    session.add(song)
    session.commit()

    assert song.id is not None
    assert song.title == "Amazing Grace"
    assert isinstance(song.added_at, datetime)
    assert isinstance(song.last_edit_at, datetime)


def test_song_required_fields(session):
    song = Song(
        title=None,
        author=None,
        added_at=datetime.now(),
        last_edit_at=datetime.now(),
    )
    session.add(song)

    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_song_default_timestamps(session, setup_related_entities):
    e = setup_related_entities

    song = Song(
        title="Grace on Time",
        author=e["author"].id,
        added_by_user_id=e["user"].id,
        search_tag_id=e["tag"].id,
        song_part_id=e["song_part"].id,
        song_order_id=e["song_order"].id,
        mscz_id=e["mscz"].id,
        user_content_id=e["user_content"].id,
        related_id=None,
        lang_tag_id=e["tag"].id,
    )
    session.add(song)
    session.commit()

    assert song.added_at is not None
    assert song.last_edit_at is not None
    assert isinstance(song.added_at, datetime)
    assert isinstance(song.last_edit_at, datetime)


def test_song_relationships_integrity(session, setup_related_entities):
    e = setup_related_entities

    song = Song(
        title="Integrity Test",
        author=e["author"].id,
        added_by_user_id=e["user"].id,
        search_tag_id=e["tag"].id,
        song_part_id=e["song_part"].id,
        song_order_id=e["song_order"].id,
        mscz_id=e["mscz"].id,
        user_content_id=e["user_content"].id,
        related_id=None,
        lang_tag_id=e["tag"].id,
    )
    session.add(song)
    session.commit()

    retrieved = session.query(Song).filter_by(id=song.id).first()
    assert retrieved is not None
    assert retrieved.author == e["author"].id
    assert retrieved.song_part_id == e["song_part"].id
    assert retrieved.song_order_id == e["song_order"].id
    assert retrieved.mscz_id == e["mscz"].id


def test_dummy(
    testclient,
):
    response = testclient.get("/song")
    assert response.status_code == 200
