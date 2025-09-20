from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import auth_settings
from app.database import DbSessionDep
from app.user.auth import get_password_hash, verify_password
from app.user.models import User
from app.user_role.models import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def authenticate_user(db, email: str, password: str) -> User:
    user = get_user(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email address",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user(
    db: DbSessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
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
    except InvalidTokenError:
        raise credentials_exception from None

    user = get_user(db, email)
    if user is None:
        raise credentials_exception
    return user


def create_user(
    session: Session,
    email: str,
    password: str,
    name: str,
    surname: str,
    mobile: str | None,
) -> User:
    role_id_sq = select(UserRole.id).where(UserRole.role == "User").scalar_subquery()

    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        surname=surname,
        mobile=mobile,
        role_id=role_id_sq,
    )

    with session.begin():
        session.add(user)
    session.refresh(user)
    return user
