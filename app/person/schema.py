from pydantic import BaseModel


class PersonCreate(BaseModel):
    name: str
    surname: str
    description: str | None = None


class PersonGet(BaseModel):
    id: int
    name: str
    surname: str
    description: str | None
