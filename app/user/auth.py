import secrets
from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import SecretStr

from app.config import auth_settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: SecretStr,
                    hashed_password: SecretStr) -> bool:
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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.secret_key,
        algorithm=auth_settings.algorithm,
    )
    return encoded_jwt


def create_refresh_token() -> str:
    """Generate a secure random refresh token."""
    return secrets.token_urlsafe(32)


def verify_refresh_token(token: str) -> bool:
    """Verify if a refresh token has a valid format."""
    # Basic check: ensure token is not empty and has reasonable length
    return bool(token and len(token) > 20)
