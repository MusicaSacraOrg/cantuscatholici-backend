import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.content_base import ContentBase
from app.models.song import Song
from app.models.static_content import StaticContent
from app.models.tag import Tag
from app.models.user import User


class FileTypeEnum(str, enum.Enum):
    mscz = "mscz"
    pdf = "pdf"

class SongArrangement(Base):
    __tablename__ = "song_arrangements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_base_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False, unique=True,
    )
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), nullable=False)
    added_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )
    added_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    file_type: Mapped[FileTypeEnum | None] = mapped_column(
        Enum(FileTypeEnum), nullable=True,
    )
    static_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("static_content.id"), nullable=True,
    )

    content_base: Mapped["ContentBase"] = relationship("ContentBase")
    song: Mapped["Song"] = relationship("Song")
    added_by_user: Mapped[Optional["User"]] = relationship("User")
    static_content: Mapped[Optional["StaticContent"]] = relationship("StaticContent")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="song_arrangement_tags")


class SongArrangementTag(Base):
    __tablename__ = "song_arrangement_tags"

    song_arrangement_id: Mapped[int] = mapped_column(
        ForeignKey("song_arrangements.id"), primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
