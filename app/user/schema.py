from datetime import datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    AliasGenerator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
)
from pydantic.alias_generators import to_camel, to_snake

from app.person.schema import PersonCreate, PersonInDb
from app.user_role.service import PredefinedUserRoles

SPECIAL_CHARS = {
    "$",
    "@",
    "#",
    "%",
    "!",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "+",
    "=",
    "{",
    "}",
    "[",
    "]",
    ":",
    '"',
}

MIN_PASSWORD_LEN = 8

PASSWORD_CHECKS = [
    (lambda s: any(c.isdigit() for c in s), "Password must contain a digit"),
    (
        lambda s: any(c.isupper() for c in s),
        "Password must contain an uppercase letter",
    ),
    (lambda s: any(c.islower() for c in s), "Password must contain a lowercase letter"),
    (
        lambda s: any(c in SPECIAL_CHARS for c in s),
        f"Password must contain a special character ({SPECIAL_CHARS})",
    ),
    (
        lambda s: len(s) >= MIN_PASSWORD_LEN,
        f"Password must be at least {MIN_PASSWORD_LEN} characters long",
    ),
]


def validate_password(password: SecretStr):
    s = password.get_secret_value()
    for check, msg in PASSWORD_CHECKS:
        if not check(s):
            raise ValueError(msg)
    return password


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserBase(BaseModel):
    email: EmailStr
    mobile: str | None = Field(default=None)
    role: str = Field(default=PredefinedUserRoles.USER)

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserCreate(PersonCreate, UserBase):
    password: Annotated[SecretStr, AfterValidator(validate_password)]


class UserRead(PersonInDb, UserBase):
    registered_at: datetime


class UserInDb(PersonInDb, UserBase):
    hashed_password: SecretStr
    registered_at: datetime
