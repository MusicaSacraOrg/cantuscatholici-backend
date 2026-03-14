
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CelebrationCategory(Base):
    __tablename__ = "celebration_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)

    celebrations: Mapped[list["Celebration"]] = relationship(
        "Celebration", back_populates="category",
    )
