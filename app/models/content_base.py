
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContentBase(Base):
    __tablename__ = 'content_base'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
