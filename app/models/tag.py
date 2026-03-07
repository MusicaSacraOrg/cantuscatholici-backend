from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.tag_category import TagCategory


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    order_index: Mapped[int] = mapped_column(nullable=False)
    tag_category_id: Mapped[int] = mapped_column(
        ForeignKey("tag_categories.id"),
        nullable=False,
    )

    category: Mapped["TagCategory"] = relationship("TagCategory", back_populates="tags")
