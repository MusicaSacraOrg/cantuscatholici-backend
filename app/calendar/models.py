from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CalendarEntry(Base):
    __tablename__ = "calendar_entry"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    recommended_song_id: Mapped[int | None] = mapped_column(
        ForeignKey("songs.id"), nullable=True
    )
