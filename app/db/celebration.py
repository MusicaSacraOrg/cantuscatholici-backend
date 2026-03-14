from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.models.celebration import Celebration, CelebrationSong

ALLOWED_ORDER_FIELDS = {
    "id": Celebration.id,
    "name": Celebration.name,
    "day": Celebration.day,
    "month": Celebration.month,
    "created_at": Celebration.created_at,
}


def db_get_celebrations(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[Celebration]]:
    total = db.execute(select(func.count()).select_from(Celebration)).scalar_one()

    stmt = select(Celebration)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_celebration_by_id(celebration_id: int, db: Session) -> Celebration | None:
    return (
        db.execute(select(Celebration).where(Celebration.id == celebration_id))
        .scalars()
        .first()
    )


def db_create_celebration(celebration: Celebration, db: Session) -> Celebration:
    db.add(celebration)
    db.commit()
    db.refresh(celebration)
    return celebration


def db_update_celebration(celebration: Celebration, db: Session) -> Celebration:
    db.commit()
    db.refresh(celebration)
    return celebration


def db_delete_celebration(celebration: Celebration, db: Session) -> Celebration:
    db.delete(celebration)
    db.commit()
    return celebration


# --- CelebrationSong ---

def db_get_celebration_songs(
    celebration_id: int,
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[CelebrationSong]]:
    CELEBRATION_SONG_ORDER = {
        "id": CelebrationSong.id,
        "order_index": CelebrationSong.order_index,
    }

    total = db.execute(
        select(func.count()).select_from(CelebrationSong).where(
            CelebrationSong.celebration_id == celebration_id,
        ),
    ).scalar_one()

    stmt = select(CelebrationSong).where(CelebrationSong.celebration_id == celebration_id)

    if order_by in CELEBRATION_SONG_ORDER:
        col = CELEBRATION_SONG_ORDER[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_celebration_song_by_id(celebration_song_id: int, db: Session) -> CelebrationSong | None:
    return (
        db.execute(select(CelebrationSong).where(CelebrationSong.id == celebration_song_id))
        .scalars()
        .first()
    )


def db_create_celebration_song(celebration_song: CelebrationSong, db: Session) -> CelebrationSong:
    db.add(celebration_song)
    db.commit()
    db.refresh(celebration_song)
    return celebration_song


def db_update_celebration_song(celebration_song: CelebrationSong, db: Session) -> CelebrationSong:
    db.commit()
    db.refresh(celebration_song)
    return celebration_song


def db_delete_celebration_song(celebration_song: CelebrationSong, db: Session) -> CelebrationSong:
    db.delete(celebration_song)
    db.commit()
    return celebration_song

