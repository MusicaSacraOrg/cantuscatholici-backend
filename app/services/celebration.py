from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.celebration import (
    db_create_celebration,
    db_create_celebration_song,
    db_delete_celebration,
    db_delete_celebration_song,
    db_get_celebration_by_id,
    db_get_celebration_song_by_id,
    db_get_celebration_songs,
    db_get_celebrations,
    db_update_celebration,
    db_update_celebration_song,
)
from app.models.celebration import Celebration, CelebrationSong
from app.schemas.celebration import (
    Celebration as CelebrationSchema,
    CelebrationCreate,
    CelebrationSong as CelebrationSongSchema,
    CelebrationSongCreate,
    CelebrationSongUpdate,
    CelebrationUpdate,
)


def get_celebrations(
    db: Session, pagination: PaginationParams,
) -> Paginated[CelebrationSchema]:
    total, items = db_get_celebrations(
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
    )
    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )


def get_celebration_by_id(celebration_id: int, db: Session) -> CelebrationSchema:
    celebration = db_get_celebration_by_id(celebration_id, db)
    if not celebration:
        raise NotFoundError("Celebration")
    return celebration


def create_celebration(data: CelebrationCreate, db: Session) -> CelebrationSchema:
    celebration = Celebration(
        name=data.name,
        description=data.description,
        celebration_category_id=data.celebration_category_id,
        day=data.day,
        month=data.month,
        created_at=datetime.now(UTC),
    )
    return db_create_celebration(celebration, db)


def update_celebration(
    celebration_id: int, data: CelebrationUpdate, db: Session,
) -> CelebrationSchema:
    celebration = db_get_celebration_by_id(celebration_id, db)
    if not celebration:
        raise NotFoundError("Celebration")
    celebration.name = data.name
    celebration.description = data.description
    celebration.celebration_category_id = data.celebration_category_id
    celebration.day = data.day
    celebration.month = data.month
    return db_update_celebration(celebration, db)


def delete_celebration(celebration_id: int, db: Session) -> CelebrationSchema:
    celebration = db_get_celebration_by_id(celebration_id, db)
    if not celebration:
        raise NotFoundError("Celebration")
    return db_delete_celebration(celebration, db)


# --- CelebrationSong ---

def get_celebration_songs(
    celebration_id: int,
    db: Session,
    pagination: PaginationParams,
) -> Paginated[CelebrationSongSchema]:
    if not db_get_celebration_by_id(celebration_id, db):
        raise NotFoundError("Celebration")

    total, items = db_get_celebration_songs(
        celebration_id,
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
    )
    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )


def get_celebration_song_by_id(celebration_song_id: int, db: Session) -> CelebrationSongSchema:
    cs = db_get_celebration_song_by_id(celebration_song_id, db)
    if not cs:
        raise NotFoundError("CelebrationSong")
    return cs


def create_celebration_song(
    celebration_id: int, data: CelebrationSongCreate, db: Session,
) -> CelebrationSongSchema:
    if not db_get_celebration_by_id(celebration_id, db):
        raise NotFoundError("Celebration")

    cs = CelebrationSong(
        celebration_id=celebration_id,
        song_id=data.song_id,
        celebration_part_id=data.celebration_part_id,
        song_part_number=data.song_part_number,
        song_part_name=data.song_part_name,
        is_prescribed=data.is_prescribed,
        liturgical_cycle=data.liturgical_cycle,
        order_index=data.order_index,
        description=data.description,
    )
    return db_create_celebration_song(cs, db)


def update_celebration_song(
    celebration_song_id: int, data: CelebrationSongUpdate, db: Session,
) -> CelebrationSongSchema:
    cs = db_get_celebration_song_by_id(celebration_song_id, db)
    if not cs:
        raise NotFoundError("CelebrationSong")

    cs.celebration_part_id = data.celebration_part_id
    cs.song_part_number = data.song_part_number
    cs.song_part_name = data.song_part_name
    cs.is_prescribed = data.is_prescribed
    cs.liturgical_cycle = data.liturgical_cycle
    cs.order_index = data.order_index
    cs.description = data.description
    return db_update_celebration_song(cs, db)


def delete_celebration_song(celebration_song_id: int, db: Session) -> CelebrationSongSchema:
    cs = db_get_celebration_song_by_id(celebration_song_id, db)
    if not cs:
        raise NotFoundError("CelebrationSong")
    return db_delete_celebration_song(cs, db)

