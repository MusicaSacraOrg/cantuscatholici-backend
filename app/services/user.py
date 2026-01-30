from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import auth_settings
from app.database import DbSessionDep
from app.schemas.person import PersonInDb
from app.services.auth import get_password_hash, verify_password
from app.exceptions.user import (
    EmailTakenException,
    InvalidCredentialsException,
    MobileTakenException,
)
from app.models.user import User
from app.schemas.user import UserInDb
from app.models.user_role import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session: Session, email: str) -> UserInDb | None:
    stmt = (
        select(User, UserRole.role).join(User.role).where(User.email == email).limit(1)
    )
    row = session.execute(stmt).first()
    if not row:
        return None

    user, role_str = row._tuple()

    # Get all Person fields from the ORM object, then enrich with User fields
    person_part = PersonInDb.model_validate(user, from_attributes=True).model_dump()

    return UserInDb.model_validate(
        {
            **person_part,  # fields from PersonInDb (id, names, etc.)
            "email": user.email,
            "mobile": user.mobile,
            "role": role_str,
            "hashed_password": user.hashed_password,
            "registered_at": user.registered_at,
        },
    )


def authenticate_user(db, email: str, password: SecretStr) -> UserInDb:
    user = get_user(db, email)
    if user is None:
        raise InvalidCredentialsException("Incorrect email or password")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException("Incorrect email or password")

    return user


async def get_current_user(
    db: DbSessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDb:
    credentials_exception = InvalidCredentialsException(
        "Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            auth_settings.secret_key,
            algorithms=[auth_settings.algorithm],
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception from e

    user = get_user(db, email)
    if user is None:
        raise credentials_exception
    return user


def create_user(
    session: Session,
    email: str,
    password: SecretStr,
    name: str,
    surname: str,
    mobile: str | None,
    description: str | None,
) -> User:
    role_id_sq = select(UserRole.id).where(UserRole.role == "User").scalar_subquery()

    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        surname=surname,
        mobile=mobile,
        role_id=role_id_sq,
        description=description,
    )

    try:
        with session.begin():
            session.add(user)
        session.refresh(user)
    except IntegrityError as e:
        # Check if it's specifically the email unique constraint
        if "email" in str(e.orig).lower():
            raise EmailTakenException("Email already in use") from e
        # Check if it's specifically the mobile unique constraint
        if "mobile" in str(e.orig).lower():
            raise MobileTakenException("Mobile number already in use") from e

        raise

    return user
