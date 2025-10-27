from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from datetime import UTC, datetime, timedelta

from app.config import auth_settings
from app.database import DbSessionDep
from app.person.schema import PersonInDb
from app.user.auth import create_refresh_token, get_password_hash, verify_password
from app.user.exceptions import (
    EmailTakenException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    MobileTakenException,
)
from app.user.models import RefreshToken, User
from app.user.schema import UserInDb
from app.user_role.models import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session: Session, email: str) -> UserInDb | None:
    stmt = (
        select(
            User,
            UserRole.role).join(
            User.role).where(
            User.email == email).limit(1)
    )
    row = session.execute(stmt).first()
    if not row:
        return None

    user, role_str = row._tuple()

    # Get all Person fields from the ORM object, then enrich with User fields
    person_part = PersonInDb.model_validate(
        user, from_attributes=True).model_dump()

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


def get_user_by_id(session: Session, user_id: int) -> UserInDb | None:
    stmt = (
        select(
            User,
            UserRole.role).join(
            User.role).where(
            User.id == user_id).limit(1)
    )
    row = session.execute(stmt).first()
    if not row:
        return None

    user, role_str = row._tuple()

    # Get all Person fields from the ORM object, then enrich with User fields
    person_part = PersonInDb.model_validate(
        user, from_attributes=True).model_dump()

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
    role_id_sq = select(
        UserRole.id).where(
        UserRole.role == "User").scalar_subquery()

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


def create_refresh_token_for_user(
        session: Session, user_id: int) -> RefreshToken:
    """Create and store a refresh token for a user."""
    refresh_token_str = create_refresh_token()
    expires_at = datetime.now(
        UTC) + timedelta(days=auth_settings.refresh_token_expire_days)

    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user_id,
        expires_at=expires_at,
    )

    session.add(refresh_token)
    session.flush()  # Flush to get ID without committing
    session.refresh(refresh_token)
    session.commit()  # Ensure the token is committed to the database

    return refresh_token


def verify_refresh_token_db(session: Session, token: str) -> RefreshToken:
    """Verify a refresh token and return it if valid."""
    stmt = select(RefreshToken).where(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).limit(1)

    refresh_token = session.execute(stmt).scalar_one_or_none()

    if not refresh_token:
        raise InvalidRefreshTokenException("Invalid refresh token")

    if refresh_token.expires_at < datetime.now(UTC):
        raise InvalidRefreshTokenException("Refresh token has expired")

    return refresh_token


def revoke_refresh_token(session: Session, token: str) -> None:
    """Revoke a refresh token."""
    stmt = select(RefreshToken).where(RefreshToken.token == token).limit(1)
    refresh_token = session.execute(stmt).scalar_one_or_none()

    if refresh_token:
        refresh_token.is_revoked = True
        # Don't commit here - let the caller handle transaction


def revoke_all_user_refresh_tokens(session: Session, user_id: int) -> None:
    """Revoke all refresh tokens for a user (useful for security events)."""
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked == False
    )
    refresh_tokens = session.execute(stmt).scalars().all()

    for token in refresh_tokens:
        token.is_revoked = True

    # Don't commit here - let the caller handle transaction
