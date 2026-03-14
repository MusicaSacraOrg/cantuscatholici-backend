from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.static_content import StaticContent


class Person(Base):
    """
    Base entity for all people (registered users and non-registered authors).
    """
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_id: Mapped[int | None] = mapped_column(
        ForeignKey("static_content.id"), nullable=True,
    )

    avatar: Mapped[Optional["StaticContent"]] = relationship("StaticContent")
