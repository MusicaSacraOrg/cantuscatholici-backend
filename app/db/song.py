from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.models.song import Song, SongPart, SongScore
from app.models.song_arrangement import SongArrangement, SongArrangementTag
from app.models.tag import Tag

ALLOWED_ORDER_FIELDS = {
    "id": Song.id,
    "title": Song.title,
    "added_at": Song.added_at,
    "last_edited_at": Song.last_edited_at,
}

ARRANGEMENT_ORDER_FIELDS = {
    "id": SongArrangement.id,
    "title": SongArrangement.title,
    "added_at": SongArrangement.added_at,
}


def db_get_songs(
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[Song]]:
    total = db.execute(select(func.count()).select_from(Song)).scalar_one()

    stmt = select(Song)

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_filter_songs(
    db: Session,
    *,
    tag_ids: list[int],
    search: str | None,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[Song]]:
    """
    Filters songs by tags and/or full-text search.

    Tag filtering rules:
    - OR within tags of the same category
    - AND across different categories

    If multiple categories are represented, the song must match at least one tag
    from EACH represented category.
    """
    stmt = select(Song)

    if tag_ids:
        # Resolve which category each tag belongs to
        tag_rows = db.execute(
            select(Tag.id, Tag.tag_category_id).where(Tag.id.in_(tag_ids)),
        ).all()

        # Group tag_ids by category
        category_to_tags: dict[int, list[int]] = {}
        for tag_id, cat_id in tag_rows:
            category_to_tags.setdefault(cat_id, []).append(tag_id)

        # For each category, song must have at least one of those tags (OR within category).
        # All categories must be satisfied (AND across categories).
        for cat_tag_ids in category_to_tags.values():
            stmt = stmt.where(
                Song.tags.any(Tag.id.in_(cat_tag_ids)),
            )

    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Song.title.ilike(pattern),
                Song.description.ilike(pattern),
            ),
        )

    total = db.execute(
        select(func.count()).select_from(stmt.subquery()),
    ).scalar_one()

    if order_by in ALLOWED_ORDER_FIELDS:
        col = ALLOWED_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_song_by_id(song_id: int, db: Session) -> Song | None:
    return db.execute(select(Song).where(Song.id == song_id)).scalars().first()


def db_create_song(song: Song, db: Session) -> Song:
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def db_update_song(song: Song, db: Session) -> Song:
    db.commit()
    db.refresh(song)
    return song


def db_delete_song(song: Song, db: Session) -> Song:
    db.delete(song)
    db.commit()
    return song


# --- SongPart ---

def db_get_parts_by_song(song_id: int, db: Session) -> list[SongPart]:
    return list(
        db.execute(
            select(SongPart).where(SongPart.song_id == song_id).order_by(SongPart.order_index),
        ).scalars().all(),
    )


def db_get_song_part_by_id(part_id: int, db: Session) -> SongPart | None:
    return db.execute(select(SongPart).where(SongPart.id == part_id)).scalars().first()


def db_create_song_part(part: SongPart, db: Session) -> SongPart:
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


def db_update_song_part(part: SongPart, db: Session) -> SongPart:
    db.commit()
    db.refresh(part)
    return part


def db_delete_song_part(part: SongPart, db: Session) -> SongPart:
    db.delete(part)
    db.commit()
    return part


# --- SongScore ---

def db_get_score_by_song(song_id: int, db: Session) -> SongScore | None:
    return db.execute(select(SongScore).where(SongScore.song_id == song_id)).scalars().first()


def db_create_song_score(score: SongScore, db: Session) -> SongScore:
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


def db_delete_song_score(score: SongScore, db: Session) -> SongScore:
    db.delete(score)
    db.commit()
    return score


# --- SongArrangement ---

def db_get_arrangements_by_song(
    song_id: int,
    db: Session,
    *,
    limit: int,
    offset: int,
    order_by: str | None = None,
    order: str = "asc",
) -> tuple[int, list[SongArrangement]]:
    total = db.execute(
        select(func.count()).select_from(SongArrangement).where(SongArrangement.song_id == song_id),
    ).scalar_one()

    stmt = select(SongArrangement).where(SongArrangement.song_id == song_id)

    if order_by in ARRANGEMENT_ORDER_FIELDS:
        col = ARRANGEMENT_ORDER_FIELDS[order_by]
        stmt = stmt.order_by(asc(col) if order == "asc" else desc(col))

    stmt = stmt.limit(limit).offset(offset)
    items = list(db.execute(stmt).scalars().all())
    return total, items


def db_get_arrangement_by_id(arrangement_id: int, db: Session) -> SongArrangement | None:
    return (
        db.execute(select(SongArrangement).where(SongArrangement.id == arrangement_id))
        .scalars()
        .first()
    )


def db_create_song_arrangement(arrangement: SongArrangement, db: Session) -> SongArrangement:
    db.add(arrangement)
    db.commit()
    db.refresh(arrangement)
    return arrangement


def db_update_song_arrangement(arrangement: SongArrangement, db: Session) -> SongArrangement:
    db.commit()
    db.refresh(arrangement)
    return arrangement


def db_delete_song_arrangement(arrangement: SongArrangement, db: Session) -> SongArrangement:
    db.delete(arrangement)
    db.commit()
    return arrangement

