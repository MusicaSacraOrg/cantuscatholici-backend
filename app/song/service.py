from collections import defaultdict

from rapidfuzz import fuzz
from sqlalchemy import delete as sa_delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.common.deps.pagination import PaginationParams
from app.person.models import Person
from app.content.models import MsczContent
from app.song.associations import song_tags
from app.song.exceptions import SongNotFoundException, SongTitleTakenException
from app.song.models import Song, SongOrder, SongPart, SongVerse
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
        all_songs = list(
            session.scalars(
                stmt.options(
                    selectinload(Song.lyrics_order)
                    .selectinload(SongOrder.part)
                    .selectinload(SongPart.verse),
                ),
            ).unique().all()
        )
        normalized_query = _normalize(search_query)

        scored = []
        for song in all_songs:
            # Title score (highest weight)
            title_score = fuzz.partial_ratio(
                normalized_query, _normalize(song.title),
            )

            # Author name score
            author_score = 0
            if song.author_person:
                author_name = f"{song.author_person.name} {song.author_person.surname}"
                author_score = fuzz.partial_ratio(
                    normalized_query, _normalize(author_name),
                )

            # Lyrics score (lower weight)
            lyrics_score = 0
            for order_entry in song.lyrics_order:
                if order_entry.part and order_entry.part.verse:
                    s = fuzz.partial_ratio(
                        normalized_query,
                        _normalize(order_entry.part.verse.lyrics),
                    )
                    lyrics_score = max(lyrics_score, s)

            # Weighted score: title > author > lyrics
            score = max(title_score, author_score * 0.9, lyrics_score * 0.7)
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
            selectinload(Song.lyrics_order),
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

    has_lyrics = len(song.lyrics_order) > 0

    mscz_content = None
    if song.mscz_id:
        mscz = session.get(MsczContent, song.mscz_id)
        if mscz:
            mscz_content = {
                "id": mscz.id,
                "svg_url": f"/api/static_content/{mscz.c_svg_file_id}",
                "pdf_url": f"/api/static_content/{mscz.pdf_file_id}",
                "mscz_url": f"/api/static_content/{mscz.c_mscz_file_id}",
                "mp3_url": f"/api/static_content/{mscz.mp3_file_id}" if mscz.mp3_file_id else None,
            }

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
        "has_lyrics": has_lyrics,
        "mscz_content": mscz_content,
    }


def create_song(
    session: Session,
    title: str,
    author_id: int,
    description: str | None = None,
    tag_ids: list[int] | None = None,
) -> dict:
    song = Song(title=title, author=author_id, description=description)
    try:
        with session.begin():
            session.add(song)
            session.flush()
            if tag_ids:
                session.execute(
                    song_tags.insert(),
                    [{"song_id": song.id, "tag_id": tid} for tid in tag_ids],
                )
    except IntegrityError as e:
        raise SongTitleTakenException("Song title already exists") from e
    return get_song_detail(session, song.id)


def update_song(
    session: Session,
    song_id: int,
    title: str,
    author_id: int,
    description: str | None = None,
    tag_ids: list[int] | None = None,
) -> dict:
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")
    try:
        with session.begin():
            song.title = title
            song.author = author_id
            song.description = description
            session.add(song)
            session.execute(
                sa_delete(song_tags).where(song_tags.c.song_id == song_id),
            )
            if tag_ids:
                session.execute(
                    song_tags.insert(),
                    [{"song_id": song_id, "tag_id": tid} for tid in tag_ids],
                )
    except IntegrityError as e:
        raise SongTitleTakenException("Song title already exists") from e
    return get_song_detail(session, song_id)


def delete_song(session: Session, song_id: int) -> None:
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")
    with session.begin():
        session.execute(
            sa_delete(song_tags).where(song_tags.c.song_id == song_id),
        )
        _delete_lyrics(session, song_id)
        session.delete(song)


def set_song_mscz(session: Session, song_id: int, mscz_id: int) -> dict:
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")
    song.mscz_id = mscz_id
    session.commit()
    return get_song_detail(session, song_id)


def get_song_lyrics(session: Session, song_id: int) -> dict:
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")

    stmt = (
        select(SongOrder)
        .where(SongOrder.song_id == song_id)
        .options(
            selectinload(SongOrder.part).selectinload(SongPart.verse),
        )
        .order_by(SongOrder.order)
    )
    orders = list(session.scalars(stmt).all())

    parts = []
    for order_entry in orders:
        part = order_entry.part
        if part is None:
            continue
        lyrics = part.verse.lyrics if part.verse else ""
        parts.append({
            "part_type": part.part_type or "",
            "lyrics": lyrics,
        })

    return {"song_id": song_id, "parts": parts}


def set_song_lyrics(
    session: Session,
    song_id: int,
    parts: list[dict],
) -> dict:
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")

    _delete_lyrics(session, song_id)

    for idx, part_data in enumerate(parts):
        verse = SongVerse(
            order=idx + 1,
            lyrics=part_data.get("lyrics", ""),
        )
        session.add(verse)
        session.flush()

        song_part = SongPart(
            part_type=part_data.get("part_type", "verse"),
            verses_id=verse.id,
        )
        session.add(song_part)
        session.flush()

        song_order = SongOrder(
            song_id=song_id,
            order=idx + 1,
            part_id=song_part.id,
        )
        session.add(song_order)

    session.commit()
    return get_song_lyrics(session, song_id)


def _delete_lyrics(session: Session, song_id: int) -> None:
    orders = list(
        session.scalars(
            select(SongOrder).where(SongOrder.song_id == song_id),
        ).all()
    )
    part_ids = [o.part_id for o in orders]

    if not orders:
        return

    verse_ids = []
    if part_ids:
        parts = list(
            session.scalars(
                select(SongPart).where(SongPart.id.in_(part_ids)),
            ).all()
        )
        verse_ids = [p.verses_id for p in parts if p.verses_id is not None]

    session.execute(
        sa_delete(SongOrder).where(SongOrder.song_id == song_id),
    )
    if part_ids:
        session.execute(
            sa_delete(SongPart).where(SongPart.id.in_(part_ids)),
        )
    if verse_ids:
        session.execute(
            sa_delete(SongVerse).where(SongVerse.id.in_(verse_ids)),
        )
