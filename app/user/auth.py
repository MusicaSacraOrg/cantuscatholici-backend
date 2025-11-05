from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import SecretStr

from app.config import auth_settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def verify_password(plain_password: SecretStr, hashed_password: SecretStr) -> bool:
    return pwd_context.verify(
        plain_password.get_secret_value(),
        hashed_password.get_secret_value(),
    )


def get_password_hash(password: SecretStr) -> str:
    return pwd_context.hash(password.get_secret_value())


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(
        minutes=auth_settings.access_token_expire_minutes,
    ),
):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(
        to_encode,
        auth_settings.secret_key,
        algorithm=auth_settings.algorithm,
    )


def create_refresh_token(
    data: dict,
    expires_delta: timedelta = timedelta(
        days=auth_settings.refresh_token_expire_days,
    ),
):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})  # ⬅️ dôležité odlíšenie
    return jwt.encode(
        to_encode,
        auth_settings.secret_key,
        algorithm=auth_settings.algorithm,
    )
