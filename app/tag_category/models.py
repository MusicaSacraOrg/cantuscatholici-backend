from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TagCategory(Base):
    __tablename__ = 'tag_categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id'), nullable=False)
    # TODO: Implement Color class or implement constraint for color format
    color: Mapped[str] = mapped_column(nullable=False)
