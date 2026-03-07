import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    common = "common"

class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)
