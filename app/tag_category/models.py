from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.tag.models import Tag


class TagCategory(Base):
    __tablename__ = "tag_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # TODO: Implement Color class or implement constraint for color format
    color: Mapped[str] = mapped_column(nullable=False)

    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="category")
