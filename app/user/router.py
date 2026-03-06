from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.types import SecretStr

from app.config import auth_settings
from app.database import DbSessionDep
from app.user.auth import create_access_token
from app.user.schema import (
    PasswordChange,
    ProfileUpdateResponse,
    Token,
    UserCreate,
    UserInDb,
    UserProfileUpdate,
    UserRead,
)
from app.user.service import (
    authenticate_user,
    change_user_password,
    create_user,
    delete_user,
    get_current_user,
    get_user_by_id,
    update_user_profile,
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


@user_router.put("/profile", response_model=ProfileUpdateResponse)
def update_profile(
    session: DbSessionDep,
    body: UserProfileUpdate,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    user = update_user_profile(
        session,
        current_user.id,
        body.name,
        body.surname,
        body.email,
        body.mobile,
        body.description,
    )
    updated = get_user_by_id(session, user.id)
    access_token = create_access_token(data={"sub": updated.email})
    return {
        "user": updated,
        "token": Token(access_token=access_token, token_type="bearer"),
    }


@user_router.put("/password", status_code=204)
def change_password(
    session: DbSessionDep,
    body: PasswordChange,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    change_user_password(
        session, current_user.id, body.old_password, body.new_password
    )


@user_router.delete("/", status_code=204)
def delete_account(
    session: DbSessionDep,
    current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    delete_user(session, current_user.id)


@user_router.get("/{user_id}", response_model=UserRead)
def get_user_detail(session: DbSessionDep, user_id: int):
    return get_user_by_id(session, user_id)
