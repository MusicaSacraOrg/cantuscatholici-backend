from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.person import Person

if TYPE_CHECKING:
    from app.models.user_role import UserRole


class User(Person):
    """Specialization of Person — a registered user with login credentials."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    mobile: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("user_roles.id"), nullable=False)
    registered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=False)

    role: Mapped["UserRole"] = relationship("UserRole")

    __mapper_args__ = {"polymorphic_identity": "user"}
