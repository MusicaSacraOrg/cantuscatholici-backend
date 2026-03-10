from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.content_base import ContentBase


class MsczContent(ContentBase):
    __tablename__ = 'mscz_content'

    id: Mapped[int] = mapped_column(
        ForeignKey('content_base.id'), primary_key=True)
    c_mscz_file_id: Mapped[int] = mapped_column(
        ForeignKey('static_content.id'), nullable=False)
    c_svg_file_id: Mapped[int] = mapped_column(
        ForeignKey('static_content.id'), nullable=False)
    pdf_file_id: Mapped[int] = mapped_column(
        ForeignKey('static_content.id'), nullable=False)
    mp3_file_id: Mapped[int | None] = mapped_column(
        ForeignKey('static_content.id'), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": "mscz_content",
    }
