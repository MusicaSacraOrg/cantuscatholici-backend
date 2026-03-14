from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.author import Author
from app.models.content_base import ContentBase
from app.models.static_content import StaticContent
from app.models.tag import Tag
from app.models.user import User


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_base_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False, unique=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    added_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )
    added_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_edited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_edit_by_user_id: Mapped[User] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )

    content_base: Mapped["ContentBase"] = relationship("ContentBase", foreign_keys=[content_base_id])
    added_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[added_by_user_id])
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="song_tags")
    authors: Mapped[list["Author"]] = relationship("Author", secondary="song_authors")
    parts: Mapped[list["SongPart"]] = relationship(
        "SongPart", back_populates="song", order_by="SongPart.order_index",
    )
    related_songs: Mapped[list["Song"]] = relationship(
        "Song",
        secondary="related_songs",
        primaryjoin="Song.id == RelatedSong.song_id",
        secondaryjoin="Song.id == RelatedSong.related_song_id",
    )


class SongAuthor(Base):
    __tablename__ = "song_authors"

    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)


class SongTag(Base):
    __tablename__ = "song_tags"

    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class RelatedSong(Base):
    __tablename__ = "related_songs"

    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    related_song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("song_id", "related_song_id", name="uq_related_song"),
    )


class SongPart(Base):
    __tablename__ = "song_parts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), nullable=False)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)  # derived from first line
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)

    song: Mapped["Song"] = relationship("Song", back_populates="parts")


class SongScore(Base):
    __tablename__ = "song_scores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_base_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False, unique=True,
    )
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), nullable=False)
    static_content_id: Mapped[int] = mapped_column(
        ForeignKey("static_content.id"), nullable=False,
    )
    added_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    content_base: Mapped["ContentBase"] = relationship("ContentBase", foreign_keys=[content_base_id])
    song: Mapped["Song"] = relationship("Song", foreign_keys=[song_id])
    static_content: Mapped["StaticContent"] = relationship("StaticContent", foreign_keys=[static_content_id])

