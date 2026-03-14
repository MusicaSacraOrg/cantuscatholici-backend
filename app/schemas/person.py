from pydantic import BaseModel, ConfigDict


class PersonBase(BaseModel):
    name: str
    surname: str
    description: str | None = None
    avatar_id: int | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class PersonInDb(PersonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

