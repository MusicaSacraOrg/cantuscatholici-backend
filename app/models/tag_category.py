from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TagCategory(Base):
    __tablename__ = "tag_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
