from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.content_base.models import ContentBase
from app.person.models import Person


class User(Person):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        ForeignKey('persons.id'), primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    mobile: Mapped[str] = mapped_column(nullable=True, unique=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('user_roles.id'), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(),
    )


class UserContent(ContentBase):
    __tablename__ = 'user_content'

    id: Mapped[int] = mapped_column(
        ForeignKey('content_base.id'), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    file_id: Mapped[int | None] = mapped_column(
        ForeignKey('static_content.id'), nullable=True)
    mscz_id: Mapped[int | None] = mapped_column(
        ForeignKey('mscz_content.id'), nullable=True)
    author: Mapped[str] = mapped_column(nullable=True)
    added_by_user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    tag_id: Mapped[int | None] = mapped_column(
        ForeignKey('tags.id'), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(),
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "user_content",
    }
