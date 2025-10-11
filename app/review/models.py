from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ReviewComment(Base):
    __tablename__ = 'review_comments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commenter_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
