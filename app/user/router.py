from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.types import SecretStr

from app.config import auth_settings
from app.database import DbSessionDep
from app.user.auth import create_access_token
from app.user.schema import Token, UserCreate, UserInDb, UserRead
from app.user.service import authenticate_user, create_user, get_current_user

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
    access_token_expires = timedelta(minutes=auth_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


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
    access_token_expires = timedelta(minutes=auth_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


# / token -> User

# /login email, password -> token

# /register email, password -> token

# /renew token -> token
