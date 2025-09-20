from datetime import datetime

from pydantic import AliasGenerator, BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel, to_snake

from app.person.schema import PersonCreate, PersonGet


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserRegister(PersonCreate):
    email: EmailStr
    password: str
    mobile: str | None = Field(default=None)

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserGet(PersonGet):
    email: EmailStr
    mobile: str | None
    role_id: int
    registered_at: datetime

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )
