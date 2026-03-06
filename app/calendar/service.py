from datetime import date

from sqlalchemy import extract, select
from sqlalchemy.orm import Session, selectinload

from app.calendar.exceptions import CalendarEntryNotFoundException
from app.calendar.models import CalendarEntry, calendar_songs
from app.song.models import Song


def _entry_to_dict(entry: CalendarEntry) -> dict:
    songs = []
    if entry.songs:
        for s in entry.songs:
            songs.append({"id": s.id, "title": s.title})

    return {
        "id": entry.id,
        "api_id": entry.api_id,
        "title": entry.title,
        "description": entry.description,
        "date": entry.date.isoformat() if entry.date else None,
        "feast_type": entry.feast_type,
        "liturgical_season": entry.liturgical_season,
        "is_recurring": entry.is_recurring,
        "songs": songs,
    }


def get_entries(
    session: Session,
    year: int | None = None,
    month: int | None = None,
    season: str | None = None,
) -> list[dict]:
    stmt = (
        select(CalendarEntry)
        .options(selectinload(CalendarEntry.songs))
        .order_by(CalendarEntry.date.asc().nulls_last())
    )
    if year:
        stmt = stmt.where(extract("year", CalendarEntry.date) == year)
    if month:
        stmt = stmt.where(extract("month", CalendarEntry.date) == month)
    if season:
        stmt = stmt.where(CalendarEntry.liturgical_season == season)

    entries = list(session.scalars(stmt).unique().all())
    return [_entry_to_dict(e) for e in entries]


def get_today(session: Session) -> list[dict]:
    today = date.today()
    stmt = (
        select(CalendarEntry)
        .where(CalendarEntry.date == today)
        .options(selectinload(CalendarEntry.songs))
    )
    entries = list(session.scalars(stmt).unique().all())
    return [_entry_to_dict(e) for e in entries]


def get_feasts(session: Session) -> list[dict]:
    stmt = (
        select(CalendarEntry)
        .where(CalendarEntry.feast_type.isnot(None))
        .options(selectinload(CalendarEntry.songs))
        .order_by(CalendarEntry.date.asc().nulls_last())
    )
    entries = list(session.scalars(stmt).unique().all())
    return [_entry_to_dict(e) for e in entries]


def get_entries_for_song(session: Session, song_id: int) -> list[dict]:
    stmt = (
        select(CalendarEntry)
        .join(calendar_songs)
        .where(calendar_songs.c.song_id == song_id)
        .options(selectinload(CalendarEntry.songs))
    )
    entries = list(session.scalars(stmt).unique().all())
    return [_entry_to_dict(e) for e in entries]


def create_entry(
    session: Session,
    api_id: str,
    title: str | None = None,
    description: str | None = None,
    entry_date: date | None = None,
    feast_type: str | None = None,
    liturgical_season: str | None = None,
    is_recurring: bool = False,
) -> dict:
    entry = CalendarEntry(
        api_id=api_id,
        title=title,
        description=description,
        date=entry_date,
        feast_type=feast_type,
        liturgical_season=liturgical_season,
        is_recurring=is_recurring,
    )
    session.add(entry)
    session.commit()
    return _entry_to_dict(entry)


def update_entry(
    session: Session,
    entry_id: int,
    title: str | None = None,
    description: str | None = None,
    entry_date: date | None = None,
    feast_type: str | None = None,
    liturgical_season: str | None = None,
) -> dict:
    entry = session.get(CalendarEntry, entry_id)
    if entry is None:
        raise CalendarEntryNotFoundException("Calendar entry not found")
    if title is not None:
        entry.title = title
    if description is not None:
        entry.description = description
    if entry_date is not None:
        entry.date = entry_date
    if feast_type is not None:
        entry.feast_type = feast_type
    if liturgical_season is not None:
        entry.liturgical_season = liturgical_season
    session.commit()
    session.refresh(entry, attribute_names=["songs"])
    return _entry_to_dict(entry)


def add_song_to_entry(session: Session, entry_id: int, song_id: int) -> dict:
    entry = session.scalars(
        select(CalendarEntry)
        .where(CalendarEntry.id == entry_id)
        .options(selectinload(CalendarEntry.songs))
    ).first()
    if entry is None:
        raise CalendarEntryNotFoundException("Calendar entry not found")
    song = session.get(Song, song_id)
    if song is None:
        raise CalendarEntryNotFoundException("Song not found")
    if song not in entry.songs:
        entry.songs.append(song)
        session.commit()
    return _entry_to_dict(entry)
