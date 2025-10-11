from enum import StrEnum

from sqlalchemy.orm import Session

from app.user_role.models import UserRole


class PredefinedUserRoles(StrEnum):
    USER = "User"
    REDACTOR = "Redactor"
    ADMIN = "Admin"


PREDEFINED_ROLES_SET = sorted(
    {
        PredefinedUserRoles.USER,
        PredefinedUserRoles.REDACTOR,
        PredefinedUserRoles.ADMIN,
    },
)


def ensure_all_exist(session: Session):
    for role in PREDEFINED_ROLES_SET:
        if session.query(UserRole).filter(UserRole.role == role).first() is None:
            session.add(UserRole(role=role))
            session.commit()
