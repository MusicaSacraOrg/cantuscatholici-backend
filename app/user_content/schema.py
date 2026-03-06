from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake

from app.common.schemas.pagination import Paginated


class UserContentCreate(BaseModel):
    title: str
    description: str | None = None
    content_type: str | None = None
    file_id: int | None = None
    mscz_id: int | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserContentUpdate(BaseModel):
    title: str
    description: str | None = None
    content_type: str | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class UserContentRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    content_type: str | None = None
    file_id: int | None = None
    mscz_id: int | None = None
    author: str | None = None
    added_by_user_id: int
    added_by_name: str | None = None
    song_id: int | None = None
    added_at: str | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


UserContentListResponse = Paginated[UserContentRead]
