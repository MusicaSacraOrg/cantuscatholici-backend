from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.content_base import ContentBase
from app.models.person import Person
from app.models.user import User


class Author(Person):
    """
    Non-registered author — linked to a Person record.
    Has its own content_base_id for review system referencing.
    """
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    content_base_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False, unique=True,
    )
    added_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )
    added_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    content_base: Mapped["ContentBase"] = relationship("ContentBase")
    person: Mapped["Person"] = relationship("Person")
    added_by_user: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[added_by_user_id],
    )
