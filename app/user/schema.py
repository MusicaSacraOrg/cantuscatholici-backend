from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.person.schema import PersonCreate, PersonGet


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRegister(PersonCreate):
    email: EmailStr
    password: str
    mobile: str | None = Field(default=None)


class UserGet(PersonGet):
    email: EmailStr
    mobile: str | None
    role_id: int
    registered_at: datetime
