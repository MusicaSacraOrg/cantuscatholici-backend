import pytest
from sqlalchemy.exc import IntegrityError

from app.calendar.models import CalendarEntry
from app.models.person import Person
from app.models.song import Song


def test_create_calendar_entry(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Test Song", author=person.id)
    session.add(song)
    session.flush()
    session.commit()

    entry = CalendarEntry(api_id="abc123",
        title="Meeting",
        description="Daily sync",
        recommended_song_id=song.id,
    )
    session.add(entry)
    session.commit()

    assert entry.id is not None
    assert entry.api_id == "abc123"
    assert entry.title == "Meeting"
    assert entry.description == "Daily sync"
    assert entry.recommended_song_id == song.id


def test_create_calendar_entry_optional_fields(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Another Song", author=person.id)
    session.add(song)
    session.commit()

    entry = CalendarEntry(api_id="xyz789", recommended_song_id=song.id)
    session.add(entry)
    session.commit()

    assert entry.title is None
    assert entry.description is None
    assert entry.recommended_song_id == song.id


def test_calendar_entry_required_fields(session):
    entry = CalendarEntry(api_id=None, recommended_song_id=None)
    session.add(entry)

    with pytest.raises(IntegrityError):
        session.commit()


def test_calendar_entry_duplicate_api_id(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Original", author=person.id)
    session.add(song)
    session.commit()

    entry1 = CalendarEntry(api_id="dup123", recommended_song_id=song.id)
    entry2 = CalendarEntry(api_id="dup123", recommended_song_id=song.id)
    session.add_all([entry1, entry2])

    with pytest.raises(IntegrityError):
        session.commit()


def test_calendar_entry_foreign_key_constraint(session):
    # Recommended song ID does not exist
    entry = CalendarEntry(api_id="ghost123", recommended_song_id=999999)
    session.add(entry)

    with pytest.raises(IntegrityError):
        session.commit()


def test_get_calendar_entry(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Test", author=person.id)
    session.add(song)
    session.commit()

    entry = CalendarEntry(api_id="read123",
        title="Read Event",
        recommended_song_id=song.id,
    )
    session.add(entry)
    session.commit()

    found = session.query(CalendarEntry).filter_by(api_id="read123").first()
    assert found is not None
    assert found.title == "Read Event"


def test_update_calendar_entry(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Old Song", author=person.id)
    session.add(song)
    session.commit()

    entry = CalendarEntry(
        api_id="upd123",
        title="Old Title",
        recommended_song_id=song.id,
    )
    session.add(entry)
    session.commit()

    entry.title = "New Title"
    entry.description = "Updated description"
    session.commit()

    updated = session.query(CalendarEntry).filter_by(id=entry.id).first()
    assert updated.title == "New Title"
    assert updated.description == "Updated description"


def test_delete_calendar_entry(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    song = Song(title="Temp Song", author=person.id)
    session.add(song)
    session.commit()

    entry = CalendarEntry(api_id="del123", recommended_song_id=song.id)
    session.add(entry)
    session.commit()

    session.delete(entry)
    session.commit()

    deleted = session.query(CalendarEntry).filter_by(id=entry.id).first()
    assert deleted is None


def test_dummy(
    testclient,
):
    response = testclient.get("/calendar")
    assert response.status_code == 200
