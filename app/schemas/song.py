from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.song_arrangement import FileTypeEnum
from app.schemas.tag import Tag as TagSchema


class SongPartBase(BaseModel):
    text: str | None = None
    title: str | None = None
    order_index: int | None = None


class SongPartCreate(SongPartBase):
    pass


class SongPartUpdate(SongPartBase):
    pass


class SongPart(SongPartBase):
    id: int
    song_id: int

    model_config = ConfigDict(from_attributes=True)


class SongScoreRead(BaseModel):
    id: int
    content_base_id: int
    song_id: int
    static_content_id: int
    added_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SongArrangementBase(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    file_type: FileTypeEnum | None = None


class SongArrangementCreate(SongArrangementBase):
    song_id: int
    tag_ids: list[int] = []


class SongArrangementUpdate(SongArrangementBase):
    tag_ids: list[int] = []


class SongArrangement(SongArrangementBase):
    id: int
    content_base_id: int
    song_id: int
    added_by_user_id: int | None = None
    added_at: datetime | None = None
    static_content_id: int | None = None
    tags: list[TagSchema] = []

    model_config = ConfigDict(from_attributes=True)


class SongBase(BaseModel):
    title: str
    description: str | None = None


class SongCreate(SongBase):
    tag_ids: list[int] = []
    author_ids: list[int] = []
    related_song_ids: list[int] = []


class SongUpdate(SongBase):
    tag_ids: list[int] = []
    author_ids: list[int] = []
    related_song_ids: list[int] = []


class Song(SongBase):
    id: int
    content_base_id: int
    added_by_user_id: int | None = None
    added_at: datetime | None = None
    last_edited_at: datetime | None = None
    tags: list[TagSchema] = []

    model_config = ConfigDict(from_attributes=True)


class SongFilterParams(BaseModel):
    tag_ids: list[int] = []
    search: str | None = None

