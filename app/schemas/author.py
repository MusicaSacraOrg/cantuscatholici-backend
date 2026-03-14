from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.person import PersonInDb


class AuthorBase(BaseModel):
    name: str
    surname: str
    description: str | None = None
    avatar_id: int | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    content_base_id: int
    added_by_user_id: int | None = None
    added_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

