from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.content_base import ContentBase
from app.models.user import User


class ReviewRequest(Base):
    __tablename__ = "review_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    editor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True,
    )
    new_entity_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False,
    )
    original_id: Mapped[int | None] = mapped_column(
        ForeignKey("content_base.id"), nullable=True,
    )
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    requester: Mapped["User"] = relationship("User", foreign_keys=[requester_id])
    editor: Mapped[Optional["User"]] = relationship("User", foreign_keys=[editor_id])
    new_entity: Mapped["ContentBase"] = relationship(
        "ContentBase", foreign_keys=[new_entity_id],
    )
    original: Mapped[Optional["ContentBase"]] = relationship(
        "ContentBase", foreign_keys=[original_id],
    )
    comments: Mapped[list["ReviewComment"]] = relationship(
        "ReviewComment", back_populates="review_request",
    )



class ReviewComment(Base):
    __tablename__ = "review_comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    review_request_id: Mapped[int] = mapped_column(
        ForeignKey("review_requests.id"), nullable=False,
    )
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    review_request: Mapped["ReviewRequest"] = relationship(
        "ReviewRequest", back_populates="comments",
    )
    created_by_user: Mapped["User"] = relationship("User")
