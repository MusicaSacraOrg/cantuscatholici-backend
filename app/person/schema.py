from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel, to_snake

from app.common.schemas.pagination import Paginated


class PersonBase(BaseModel):
    name: str
    surname: str
    description: str | None = Field(default=None)

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class PersonCreate(PersonBase):
    pass


class PersonInDb(PersonBase):
    id: int


PersonList = Paginated[PersonInDb]
