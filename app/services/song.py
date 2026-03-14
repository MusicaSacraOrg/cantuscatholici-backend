from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import AlreadyExistsError, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.song import (
    db_create_song,
    db_create_song_arrangement,
    db_create_song_part,
    db_create_song_score,
    db_delete_song,
    db_delete_song_arrangement,
    db_delete_song_part,
    db_delete_song_score,
    db_filter_songs,
    db_get_arrangement_by_id,
    db_get_arrangements_by_song,
    db_get_score_by_song,
    db_get_song_by_id,
    db_get_song_part_by_id,
    db_get_parts_by_song,
    db_get_songs,
    db_update_song,
    db_update_song_arrangement,
    db_update_song_part,
)
from app.models.content_base import ContentBase
from app.models.song import Song, SongPart, SongScore
from app.models.song_arrangement import SongArrangement
from app.models.tag import Tag
from app.schemas.song import (
    Song as SongSchema,
    SongArrangement as SongArrangementSchema,
    SongArrangementCreate,
    SongArrangementUpdate,
    SongCreate,
    SongFilterParams,
    SongPart as SongPartSchema,
    SongPartCreate,
    SongPartUpdate,
    SongScoreRead,
    SongUpdate,
)


def _resolve_tags(tag_ids: list[int], db: Session) -> list[Tag]:
    if not tag_ids:
        return []
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    if len(tags) != len(tag_ids):
        raise NotFoundError("Tag")
    return tags


def _resolve_songs(song_ids: list[int], db: Session) -> list[Song]:
    if not song_ids:
        return []
    songs = db.query(Song).filter(Song.id.in_(song_ids)).all()
    return songs


# --- Song ---

def get_songs(db: Session, pagination: PaginationParams) -> Paginated[SongSchema]:
    total, items = db_get_songs(
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


def filter_songs(
    params: SongFilterParams,
    db: Session,
    pagination: PaginationParams,
) -> Paginated[SongSchema]:
    total, items = db_filter_songs(
        db,
        tag_ids=params.tag_ids,
        search=params.search,
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


def get_song_by_id(song_id: int, db: Session) -> SongSchema:
    song = db_get_song_by_id(song_id, db)
    if not song:
        raise NotFoundError("Song")
    return song


def create_song(data: SongCreate, added_by_user_id: int, db: Session) -> SongSchema:
    content_base = ContentBase()
    db.add(content_base)
    db.flush()

    tags = _resolve_tags(data.tag_ids, db)
    related_songs = _resolve_songs(data.related_song_ids, db)

    from app.models.author import Author  # avoid circular at module level
    authors = db.query(Author).filter(Author.id.in_(data.author_ids)).all() if data.author_ids else []

    song = Song(
        content_base_id=content_base.id,
        title=data.title,
        description=data.description,
        added_by_user_id=added_by_user_id,
        added_at=datetime.now(UTC),
        tags=tags,
        authors=authors,
        related_songs=related_songs,
    )

    try:
        return db_create_song(song, db)
    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e.orig).lower():
            raise AlreadyExistsError("Song") from e
        raise


def update_song(song_id: int, data: SongUpdate, added_by_user_id: int, db: Session) -> SongSchema:
    song = db_get_song_by_id(song_id, db)
    if not song:
        raise NotFoundError("Song")

    tags = _resolve_tags(data.tag_ids, db)
    related_songs = _resolve_songs(data.related_song_ids, db)

    from app.models.author import Author
    authors = db.query(Author).filter(Author.id.in_(data.author_ids)).all() if data.author_ids else []

    song.title = data.title
    song.description = data.description
    song.last_edited_at = datetime.now(UTC)
    song.last_edit_by_user_id = added_by_user_id
    song.tags = tags
    song.authors = authors
    song.related_songs = related_songs

    try:
        return db_update_song(song, db)
    except IntegrityError as e:
        db.rollback()
        if "unique" in str(e.orig).lower():
            raise AlreadyExistsError("Song") from e
        raise


def delete_song(song_id: int, db: Session) -> SongSchema:
    song = db_get_song_by_id(song_id, db)
    if not song:
        raise NotFoundError("Song")
    return db_delete_song(song, db)


# --- SongPart ---

def get_song_parts(song_id: int, db: Session) -> list[SongPartSchema]:
    if not db_get_song_by_id(song_id, db):
        raise NotFoundError("Song")
    return db_get_parts_by_song(song_id, db)


def get_song_part_by_id(part_id: int, db: Session) -> SongPartSchema:
    part = db_get_song_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("SongPart")
    return part


def create_song_part(song_id: int, data: SongPartCreate, db: Session) -> SongPartSchema:
    if not db_get_song_by_id(song_id, db):
        raise NotFoundError("Song")

    part = SongPart(
        song_id=song_id,
        text=data.text,
        title=data.title,
        order_index=data.order_index,
    )
    return db_create_song_part(part, db)


def update_song_part(part_id: int, data: SongPartUpdate, db: Session) -> SongPartSchema:
    part = db_get_song_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("SongPart")

    part.text = data.text
    part.title = data.title
    part.order_index = data.order_index
    return db_update_song_part(part, db)


def delete_song_part(part_id: int, db: Session) -> SongPartSchema:
    part = db_get_song_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("SongPart")
    return db_delete_song_part(part, db)


# --- SongScore ---

def get_song_score(song_id: int, db: Session) -> SongScoreRead:
    score = db_get_score_by_song(song_id, db)
    if not score:
        raise NotFoundError("SongScore")
    return score


def create_song_score(
    song_id: int,
    static_content_id: int,
    db: Session,
) -> SongScoreRead:
    if not db_get_song_by_id(song_id, db):
        raise NotFoundError("Song")

    existing = db_get_score_by_song(song_id, db)
    if existing:
        raise AlreadyExistsError("SongScore")

    content_base = ContentBase()
    db.add(content_base)
    db.flush()

    score = SongScore(
        content_base_id=content_base.id,
        song_id=song_id,
        static_content_id=static_content_id,
        added_at=datetime.now(UTC),
    )
    return db_create_song_score(score, db)


def delete_song_score(song_id: int, db: Session) -> SongScoreRead:
    score = db_get_score_by_song(song_id, db)
    if not score:
        raise NotFoundError("SongScore")
    return db_delete_song_score(score, db)


# --- SongArrangement ---

def get_song_arrangements(
    song_id: int,
    db: Session,
    pagination: PaginationParams,
) -> Paginated[SongArrangementSchema]:
    if not db_get_song_by_id(song_id, db):
        raise NotFoundError("Song")

    total, items = db_get_arrangements_by_song(
        song_id,
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


def get_song_arrangement_by_id(arrangement_id: int, db: Session) -> SongArrangementSchema:
    arr = db_get_arrangement_by_id(arrangement_id, db)
    if not arr:
        raise NotFoundError("SongArrangement")
    return arr


def create_song_arrangement(
    data: SongArrangementCreate,
    added_by_user_id: int,
    db: Session,
) -> SongArrangementSchema:
    if not db_get_song_by_id(data.song_id, db):
        raise NotFoundError("Song")

    tags = _resolve_tags(data.tag_ids, db)

    content_base = ContentBase()
    db.add(content_base)
    db.flush()

    arrangement = SongArrangement(
        content_base_id=content_base.id,
        song_id=data.song_id,
        title=data.title,
        author=data.author,
        description=data.description,
        file_type=data.file_type,
        added_by_user_id=added_by_user_id,
        added_at=datetime.now(UTC),
        tags=tags,
    )
    return db_create_song_arrangement(arrangement, db)


def update_song_arrangement(
    arrangement_id: int,
    data: SongArrangementUpdate,
    db: Session,
) -> SongArrangementSchema:
    arr = db_get_arrangement_by_id(arrangement_id, db)
    if not arr:
        raise NotFoundError("SongArrangement")

    tags = _resolve_tags(data.tag_ids, db)

    arr.title = data.title
    arr.author = data.author
    arr.description = data.description
    arr.file_type = data.file_type
    arr.tags = tags

    return db_update_song_arrangement(arr, db)


def delete_song_arrangement(arrangement_id: int, db: Session) -> SongArrangementSchema:
    arr = db_get_arrangement_by_id(arrangement_id, db)
    if not arr:
        raise NotFoundError("SongArrangement")
    return db_delete_song_arrangement(arr, db)

