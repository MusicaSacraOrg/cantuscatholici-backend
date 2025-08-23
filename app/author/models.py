from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.person.models import Person


class Author(Person):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(
        ForeignKey('persons.id'), primary_key=True)
    added_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(),
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "authors",
    }
