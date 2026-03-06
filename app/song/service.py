from collections import defaultdict

from rapidfuzz import fuzz
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.common.deps.pagination import PaginationParams
from app.person.models import Person
from app.song.associations import song_tags
from app.song.exceptions import SongNotFoundException
from app.song.models import Song
from app.tag.models import Tag
from app.tag_category.models import TagCategory

try:
    from unidecode import unidecode
except ImportError:
    def unidecode(s: str) -> str:
        return s

FUZZY_THRESHOLD = 60


def _normalize(text: str) -> str:
    return unidecode(text).lower()


def get_songs(
    session: Session,
    pagination: PaginationParams,
    tag_ids: list[int] | None = None,
    search_query: str | None = None,
    sort_by: str | None = None,
    sort_dir: str | None = None,
) -> dict:
    stmt = (
        select(Song)
        .options(
            selectinload(Song.tags).selectinload(Tag.category),
            selectinload(Song.author_person),
        )
    )
    count_stmt = select(func.count()).select_from(Song)

    # Tag filtering: AND between categories, OR within category
    if tag_ids:
        # Group tags by category
        tag_rows = session.execute(
            select(Tag.id, Tag.category_id).where(Tag.id.in_(tag_ids)),
        ).all()
        categories: dict[int, list[int]] = defaultdict(list)
        for tid, cid in tag_rows:
            categories[cid].append(tid)

        # For each category, require the song to have at least one of the tags
        for cat_tag_ids in categories.values():
            subq = (
                select(song_tags.c.song_id)
                .where(song_tags.c.tag_id.in_(cat_tag_ids))
            ).correlate(Song)
            stmt = stmt.where(Song.id.in_(subq))
            count_stmt = count_stmt.where(Song.id.in_(subq))

    # Sort
    if sort_by == "title":
        order = Song.title.desc() if sort_dir == "desc" else Song.title.asc()
    else:
        order = Song.title.asc()
    stmt = stmt.order_by(order)

    if search_query:
        # Fuzzy search: load all matching candidates, then filter in Python
        all_songs = list(session.scalars(stmt).unique().all())
        normalized_query = _normalize(search_query)

        scored = []
        for song in all_songs:
            title_score = fuzz.partial_ratio(
                normalized_query, _normalize(song.title),
            )
            score = title_score
            if score >= FUZZY_THRESHOLD:
                scored.append((score, song))

        scored.sort(key=lambda x: x[0], reverse=True)
        total = len(scored)
        page_songs = scored[pagination.offset:pagination.offset + pagination.limit]
        items = [_song_to_dict(s) for _, s in page_songs]
    else:
        total = session.scalar(count_stmt)
        songs = (
            session.scalars(
                stmt.offset(pagination.offset).limit(pagination.limit),
            ).unique().all()
        )
        items = [_song_to_dict(s) for s in songs]

    return {
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset,
        "items": items,
    }


def _song_to_dict(song: Song) -> dict:
    author_name = None
    if song.author_person:
        p = song.author_person
        author_name = f"{p.name} {p.surname}".strip()

    tag_list = []
    for tag in song.tags:
        tag_list.append({
            "id": tag.id,
            "name": tag.name,
            "category_color": tag.category.color if tag.category else "",
        })

    desc = song.description
    if desc and len(desc) > 200:
        desc = desc[:200] + "..."

    return {
        "id": song.id,
        "title": song.title,
        "author_name": author_name,
        "tags": tag_list,
        "description": desc,
    }


def get_song_detail(session: Session, song_id: int) -> dict:
    stmt = (
        select(Song)
        .where(Song.id == song_id)
        .options(
            selectinload(Song.tags).selectinload(Tag.category),
            selectinload(Song.author_person),
        )
    )
    song = session.scalars(stmt).unique().first()
    if song is None:
        raise SongNotFoundException("Song not found")

    author_name = None
    author_id = None
    if song.author_person:
        p = song.author_person
        author_name = f"{p.name} {p.surname}".strip()
        author_id = p.id

    tag_list = []
    for tag in song.tags:
        tag_list.append({
            "id": tag.id,
            "name": tag.name,
            "category_id": tag.category_id,
            "category_name": tag.category.name if tag.category else "",
            "category_color": tag.category.color if tag.category else "",
        })

    related_song = None
    if song.related_id:
        related = session.get(Song, song.related_id)
        if related:
            related_song = {"id": related.id, "title": related.title}

    return {
        "id": song.id,
        "title": song.title,
        "author_name": author_name,
        "author_id": author_id,
        "description": song.description,
        "tags": tag_list,
        "related_song": related_song,
        "added_at": song.added_at.isoformat() if song.added_at else None,
        "last_edit_at": song.last_edit_at.isoformat() if song.last_edit_at else None,
    }
