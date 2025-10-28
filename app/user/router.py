from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.types import SecretStr

from app.config import auth_settings
from app.database import DbSessionDep
from app.user.auth import create_access_token
from app.user.schema import RefreshTokenRequest, Token, UserCreate, UserInDb, UserRead
from app.user.service import (
    authenticate_user,
    create_refresh_token_for_user,
    create_user,
    get_current_user,
    revoke_refresh_token,
    verify_refresh_token_db,
)

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/", response_model=UserRead)
async def me(
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return current_user


@user_router.post("/login")
async def login(
    session: DbSessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    secret_password = SecretStr(form_data.password)
    user = authenticate_user(session, form_data.username, secret_password)
    access_token_expires = timedelta(
        minutes=auth_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    # Create and store refresh token
    refresh_token_obj = create_refresh_token_for_user(session, user.id)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token_obj.token,
        token_type="bearer"
    )


@user_router.post("/register")
async def register(
    session: DbSessionDep,
    new_user: UserCreate,
) -> Token:
    user = create_user(
        session=session,
        email=new_user.email,
        password=new_user.password,
        name=new_user.name,
        surname=new_user.surname,
        mobile=new_user.mobile,
        description=new_user.description,
    )
    access_token_expires = timedelta(
        minutes=auth_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    # Create and store refresh token
    refresh_token_obj = create_refresh_token_for_user(session, user.id)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token_obj.token,
        token_type="bearer"
    )


# / token -> User

# /login email, password -> token

# /register email, password -> token

# /renew token -> token


@user_router.post("/refresh")
async def refresh(session: DbSessionDep,
                  request: RefreshTokenRequest) -> Token:
    """Exchange a refresh token for a new access token and refresh token."""
    try:
        # Verify the refresh token FIRST (before any modifications)
        refresh_token_obj = verify_refresh_token_db(
            session, request.refresh_token)

        # Get the user associated with the refresh token
        from app.user.service import get_user_by_id
        user = get_user_by_id(session, refresh_token_obj.user_id)

        if not user:
            from app.user.exceptions import InvalidRefreshTokenException
            raise InvalidRefreshTokenException("User not found")

        # Generate new access token
        access_token_expires = timedelta(
            minutes=auth_settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires,
        )

        # Revoke the old refresh token FIRST (before creating new one)
        revoke_refresh_token(session, request.refresh_token)

        # Create and store new refresh token
        new_refresh_token_obj = create_refresh_token_for_user(session, user.id)

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token_obj.token,
            token_type="bearer",
        )
    except Exception:
        # Rollback on any error to prevent partial state
        session.rollback()
        raise
