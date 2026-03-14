
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.content_base import ContentBase


class StaticContent(Base):
    __tablename__ = 'static_content'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_base_id: Mapped[int] = mapped_column(
        ForeignKey("content_base.id"), nullable=False,
    )
    path: Mapped[str] = mapped_column(unique=True, nullable=False)

    content_base: Mapped["ContentBase"] = relationship("ContentBase")
