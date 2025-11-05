from typing import ClassVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.content_base.models import ContentBase


class StaticContent(ContentBase):
    __tablename__ = "static_content"

    id: Mapped[int] = mapped_column(ForeignKey("content_base.id"), primary_key=True)
    path: Mapped[str] = mapped_column(unique=True, nullable=False)

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "static_content",
    }
