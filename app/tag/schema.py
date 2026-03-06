from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake

from app.common.schemas.pagination import Paginated


class TagBase(BaseModel):
    name: str
    category_id: int

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class TagReadWithCategory(TagRead):
    category_name: str
    category_color: str


TagList = Paginated[TagRead]
