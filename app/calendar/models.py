from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.song.models import Song

calendar_songs = Table(
    "calendar_songs",
    Base.metadata,
    Column("calendar_entry_id", ForeignKey("calendar_entry.id"), primary_key=True),
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
)


class CalendarEntry(Base):
    __tablename__ = 'calendar_entry'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    recommended_song_id: Mapped[int | None] = mapped_column(
        ForeignKey('songs.id'), nullable=True)
    date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    feast_type: Mapped[str | None] = mapped_column(nullable=True)
    liturgical_season: Mapped[str | None] = mapped_column(nullable=True)
    is_recurring: Mapped[bool] = mapped_column(nullable=False, server_default="false")

    songs: Mapped[list["Song"]] = relationship("Song", secondary=calendar_songs)
