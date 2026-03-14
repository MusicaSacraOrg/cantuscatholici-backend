import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.celebration_category import CelebrationCategory
from app.models.celebration_part import CelebrationPart
from app.models.song import Song


class LiturgicalCycleEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"

class Celebration(Base):
    __tablename__ = "celebrations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    celebration_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("celebration_categories.id"), nullable=True,
    )
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    month: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    category: Mapped[Optional["CelebrationCategory"]] = relationship(
        "CelebrationCategory", back_populates="celebrations",
    )
    songs: Mapped[list["CelebrationSong"]] = relationship(
        "CelebrationSong", back_populates="celebration",
    )


class CelebrationSong(Base):
    __tablename__ = "celebration_songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    celebration_id: Mapped[int] = mapped_column(
        ForeignKey("celebrations.id"), nullable=False,
    )
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"), nullable=False)
    celebration_part_id: Mapped[int | None] = mapped_column(
        ForeignKey("celebration_parts.id"), nullable=True,
    )
    song_part_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    song_part_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_prescribed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    liturgical_cycle: Mapped[LiturgicalCycleEnum | None] = mapped_column(
        Enum(LiturgicalCycleEnum), nullable=True,
    )
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    celebration: Mapped["Celebration"] = relationship(
        "Celebration", back_populates="songs",
    )
    song: Mapped["Song"] = relationship("Song")
    celebration_part: Mapped[Optional["CelebrationPart"]] = relationship(
        "CelebrationPart",
    )
