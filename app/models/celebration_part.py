
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CelebrationPart(Base):
    __tablename__ = "celebration_parts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    order_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
