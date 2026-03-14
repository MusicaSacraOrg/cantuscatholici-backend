from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.celebration import LiturgicalCycleEnum


class CelebrationSongBase(BaseModel):
    celebration_id: int
    song_id: int
    celebration_part_id: int | None = None
    song_part_number: int | None = None
    song_part_name: str | None = None
    is_prescribed: bool | None = None
    liturgical_cycle: LiturgicalCycleEnum | None = None
    order_index: int | None = None
    description: str | None = None


class CelebrationSongCreate(CelebrationSongBase):
    pass


class CelebrationSongUpdate(BaseModel):
    celebration_part_id: int | None = None
    song_part_number: int | None = None
    song_part_name: str | None = None
    is_prescribed: bool | None = None
    liturgical_cycle: LiturgicalCycleEnum | None = None
    order_index: int | None = None
    description: str | None = None


class CelebrationSong(CelebrationSongBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CelebrationBase(BaseModel):
    name: str | None = None
    description: str | None = None
    celebration_category_id: int | None = None
    day: int | None = None
    month: int | None = None


class CelebrationCreate(CelebrationBase):
    pass


class CelebrationUpdate(CelebrationBase):
    pass


class Celebration(CelebrationBase):
    id: int
    created_at: datetime | None = None
    songs: list[CelebrationSong] = []

    model_config = ConfigDict(from_attributes=True)

