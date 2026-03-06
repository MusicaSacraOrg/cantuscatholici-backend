from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake

from app.common.schemas.pagination import Paginated


class SongTagItem(BaseModel):
    id: int
    name: str
    category_color: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class SongListItem(BaseModel):
    id: int
    title: str
    author_name: str | None = None
    tags: list[SongTagItem] = []
    description: str | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


SongListResponse = Paginated[SongListItem]


class SongTagDetailItem(BaseModel):
    id: int
    name: str
    category_id: int
    category_name: str
    category_color: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class RelatedSong(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class SongCreate(BaseModel):
    title: str
    author_id: int
    description: str | None = None
    tag_ids: list[int] = []

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class SongUpdate(BaseModel):
    title: str
    author_id: int
    description: str | None = None
    tag_ids: list[int] = []

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class SongDetail(BaseModel):
    id: int
    title: str
    author_name: str | None = None
    author_id: int | None = None
    description: str | None = None
    tags: list[SongTagDetailItem] = []
    related_song: RelatedSong | None = None
    added_at: str | None = None
    last_edit_at: str | None = None
    has_lyrics: bool = False

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class LyricsPartItem(BaseModel):
    part_type: str
    lyrics: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class SongLyrics(BaseModel):
    song_id: int
    parts: list[LyricsPartItem] = []

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class LyricsUpdate(BaseModel):
    parts: list[LyricsPartItem]

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )
