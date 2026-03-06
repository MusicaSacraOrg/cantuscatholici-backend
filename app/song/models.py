from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.content_base.models import ContentBase
from app.database import Base
from app.song.associations import song_tags

if TYPE_CHECKING:
    from app.person.models import Person
    from app.tag.models import Tag


class Song(ContentBase):
    __tablename__ = 'songs'

    id: Mapped[int] = mapped_column(
        ForeignKey('content_base.id'), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[int] = mapped_column(
        ForeignKey('persons.id'), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    added_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'), nullable=True)
    search_tag_id: Mapped[int | None] = mapped_column(
        ForeignKey('tags.id'), nullable=True)
    song_part_id: Mapped[int | None] = mapped_column(
        ForeignKey('song_parts.id'), nullable=True)
    song_order_id: Mapped[int | None] = mapped_column(
        ForeignKey('song_order.id'), nullable=True)
    mscz_id: Mapped[int | None] = mapped_column(
        ForeignKey('mscz_content.id'), nullable=True)
    user_content_id: Mapped[int | None] = mapped_column(
        ForeignKey('user_content.id'), nullable=True)
    related_id: Mapped[int | None] = mapped_column(
        ForeignKey('songs.id'), nullable=True)
    lang_tag_id: Mapped[int | None] = mapped_column(
        ForeignKey('tags.id'), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    last_edit_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=song_tags)
    author_person: Mapped["Person"] = relationship("Person", foreign_keys=[author])
    lyrics_order: Mapped[list["SongOrder"]] = relationship(
        "SongOrder", back_populates="song", order_by="SongOrder.order",
        foreign_keys="SongOrder.song_id",
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "songs",
    }


class SongOrder(Base):
    __tablename__ = 'song_order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    song_id: Mapped[int | None] = mapped_column(
        ForeignKey('songs.id'), nullable=True)
    order: Mapped[int] = mapped_column(nullable=False)
    part_id: Mapped[int] = mapped_column(
        ForeignKey('song_parts.id'), nullable=False)

    song: Mapped["Song"] = relationship(
        "Song", back_populates="lyrics_order", foreign_keys=[song_id],
    )
    part: Mapped["SongPart"] = relationship("SongPart")


class SongPart(Base):
    __tablename__ = 'song_parts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag_id: Mapped[int | None] = mapped_column(
        ForeignKey('tags.id'), nullable=True)
    part_type: Mapped[str | None] = mapped_column(nullable=True)
    verses_id: Mapped[int | None] = mapped_column(
        ForeignKey('song_verses.id'), nullable=True)

    verse: Mapped["SongVerse | None"] = relationship("SongVerse")


class SongVerse(Base):
    __tablename__ = 'song_verses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(nullable=False)
    lyrics: Mapped[str] = mapped_column(nullable=False)


class SongMr(Base):
    __tablename__ = 'song_mr'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reviewable_id: Mapped[int] = mapped_column(
        ForeignKey('content_base.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    redactor_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    comments: Mapped[int | None] = mapped_column(
        ForeignKey('review_comments.id'), nullable=True)
    closed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
