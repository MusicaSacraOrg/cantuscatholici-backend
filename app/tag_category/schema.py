from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake

from app.common.schemas.pagination import Paginated


class TagCategoryBase(BaseModel):
    name: str
    color: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class TagCategoryCreate(TagCategoryBase):
    pass


class TagCategoryUpdate(TagCategoryBase):
    pass


class TagCategoryRead(TagCategoryBase):
    id: int


class TagReadNested(BaseModel):
    id: int
    name: str
    category_id: int

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class TagCategoryWithTags(TagCategoryRead):
    tags: list[TagReadNested]


TagCategoryList = Paginated[TagCategoryRead]
