from datetime import datetime
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.content_base.models import ContentBase
from app.database import Base
from app.person.models import Person

if TYPE_CHECKING:
    from app.user_role.models import UserRole


class User(Person):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        ForeignKey('persons.id'), primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    mobile: Mapped[str] = mapped_column(nullable=True, unique=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('user_roles.id'), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # relationships
    role: Mapped["UserRole"] = relationship("UserRole", back_populates="users")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
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
        server_default=func.now(),
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "user_content",
    }


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    is_revoked: Mapped[bool] = mapped_column(nullable=False, default=False)

    # relationship
    user: Mapped["User"] = relationship(
        "User", back_populates="refresh_tokens")
