from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from pydantic.types import SecretStr

from app.config import auth_settings
from app.database import DbSessionDep
from app.user.auth import create_access_token, create_refresh_token
from app.user.exceptions import InvalidCredentialsException
from app.user.schema import (
    RefreshRequest,
    Token,
    TokenWithRefresh,
    UserCreate,
    UserInDb,
    UserRead,
)
from app.user.service import authenticate_user, create_user, get_current_user, get_user

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
) -> TokenWithRefresh:
    secret_password = SecretStr(form_data.password)
    user = authenticate_user(session, form_data.username, secret_password)
    access_token_expires = timedelta(minutes=auth_settings.access_token_expire_minutes)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    refresh_token = create_refresh_token(
        data={"sub": user.email},
    )

    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@user_router.post("/register")
async def register(
    session: DbSessionDep,
    new_user: UserCreate,
) -> TokenWithRefresh:
    user = create_user(
        session=session,
        email=new_user.email,
        password=new_user.password,
        name=new_user.name,
        surname=new_user.surname,
        mobile=new_user.mobile,
        description=new_user.description,
    )
    access_token_expires = timedelta(minutes=auth_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email},
    )

    return TokenWithRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@user_router.post("/renew")
async def renew_token(
    body: RefreshRequest,
    session: DbSessionDep,
) -> Token:
    try:
        payload = jwt.decode(
            body.refresh_token,
            auth_settings.secret_key,
            algorithms=[auth_settings.algorithm],
        )
        # token type check
        if payload.get("type") != "refresh":
            raise InvalidCredentialsException("Wrong token type")

        sub = payload.get("sub")
        if not sub:
            raise InvalidCredentialsException("Invalid token")

    except InvalidTokenError as e:
        raise InvalidCredentialsException("Invalid refresh token") from e

    # user check
    user = get_user(session, sub)
    if user is None:
        raise InvalidCredentialsException("User not found")

    new_access_token = create_access_token(data={"sub": sub})
    return Token(access_token=new_access_token, token_type="bearer")


# / token -> User

# /login email, password -> token

# /register email, password -> token

# /renew token -> token
