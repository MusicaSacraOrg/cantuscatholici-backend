"""Seed script to populate test data for development.

Run inside the Docker container:
    docker compose exec cantuscatholici-api python -m app.seed
"""

from sqlalchemy import select

import app.models  # noqa: F401  — registers all ORM models
from app.database import SessionLocal
from app.person.models import Person
from app.song.associations import song_tags
from app.song.models import Song
from app.tag.models import Tag
from app.tag_category.models import TagCategory

TAG_CATEGORIES = [
    {"name": "Liturgický rok", "color": "purple"},
    {"name": "Časti omše", "color": "blue"},
    {"name": "Ordinárium", "color": "green"},
    {"name": "Slávnosti", "color": "red"},
    {"name": "Typ", "color": "orange"},
    {"name": "Spevníky", "color": "teal"},
    {"name": "Jazyk", "color": "gray"},
    {"name": "Inštrumentálne", "color": "yellow"},
]

TAGS_BY_CATEGORY = {
    "Liturgický rok": ["Advent", "Vianoce", "Pôst", "Veľká noc", "Cezročné obdobie"],
    "Časti omše": ["Introit", "Offertorium", "Communio", "Záverečná"],
    "Ordinárium": ["Kyrie", "Gloria", "Sanctus", "Agnus Dei"],
    "Slávnosti": ["Mariánske", "Svätí", "Ďakovné"],
    "Typ": ["Hymnus", "Žalm", "Sekvencia", "Antifóna"],
    "Spevníky": ["JKS", "Jednotný katolícky spevník"],
    "Jazyk": ["Slovenčina", "Latinčina", "Čeština"],
    "Inštrumentálne": ["Organ", "Gitara", "A capella"],
}

AUTHORS = [
    {"name": "Mikuláš", "surname": "Schneider-Trnavský"},
    {"name": "Ján", "surname": "Levoslav Bella"},
    {"name": "Juraj", "surname": "Tranovský"},
]

SONGS = [
    {
        "title": "Ty si Pane v každom chráme",
        "author_idx": 0,
        "description": "Obľúbená pieseň zo spevníka JKS č. 257.",
        "tag_names": ["Introit", "JKS", "Slovenčina", "Organ"],
    },
    {
        "title": "Kto za pravdu horí",
        "author_idx": 0,
        "description": "Pieseň o pravde a viere.",
        "tag_names": ["Hymnus", "JKS", "Slovenčina"],
    },
    {
        "title": "Aleluja, chváľte Pána",
        "author_idx": 1,
        "description": "Radostná veľkonočná pieseň.",
        "tag_names": ["Veľká noc", "Gloria", "Slovenčina", "A capella"],
    },
    {
        "title": "Ó Mária bolestivá",
        "author_idx": 0,
        "description": "Mariánska pieseň počas pôstneho obdobia.",
        "tag_names": ["Pôst", "Mariánske", "Slovenčina", "Organ"],
    },
    {
        "title": "Veni Creator Spiritus",
        "author_idx": 2,
        "description": "Latinský hymnus k Duchu Svätému.",
        "tag_names": ["Hymnus", "Latinčina", "A capella"],
    },
    {
        "title": "Svätý, svätý, svätý",
        "author_idx": 1,
        "description": "Ordinárium - Sanctus v slovenčine.",
        "tag_names": ["Sanctus", "Slovenčina", "Organ"],
    },
    {
        "title": "Baránok Boží",
        "author_idx": 0,
        "description": "Ordinárium - Agnus Dei v slovenčine.",
        "tag_names": ["Agnus Dei", "Slovenčina", "Organ"],
    },
    {
        "title": "Tichá noc",
        "author_idx": 2,
        "description": "Známa vianočná pieseň.",
        "tag_names": ["Vianoce", "Slovenčina", "Gitara"],
    },
    {
        "title": "Pange lingua gloriosi",
        "author_idx": 2,
        "description": "Slávny latinský hymnus o Eucharistii.",
        "tag_names": ["Hymnus", "Latinčina", "A capella", "Svätí"],
    },
    {
        "title": "Príď Duchu Svätý príď",
        "author_idx": 1,
        "description": "Sekvencia k Duchu Svätému pre Turíce.",
        "tag_names": ["Sekvencia", "Slovenčina", "Organ", "Ďakovné"],
    },
]


def seed():
    with SessionLocal() as session:
        # Check if data already exists
        existing = session.scalar(select(TagCategory).limit(1))
        if existing:
            print("Data already seeded. Skipping.")
            return

        # Create tag categories
        cat_map: dict[str, TagCategory] = {}
        for cat_data in TAG_CATEGORIES:
            cat = TagCategory(**cat_data)
            session.add(cat)
            cat_map[cat_data["name"]] = cat
        session.flush()

        # Create tags
        tag_map: dict[str, Tag] = {}
        for cat_name, tag_names in TAGS_BY_CATEGORY.items():
            cat = cat_map[cat_name]
            for tag_name in tag_names:
                tag = Tag(name=tag_name, category_id=cat.id)
                session.add(tag)
                tag_map[tag_name] = tag
        session.flush()

        # Create authors (as Person records)
        authors: list[Person] = []
        for author_data in AUTHORS:
            person = Person(**author_data)
            session.add(person)
            authors.append(person)
        session.flush()

        # Create songs (Song inherits ContentBase via polymorphic joined table)
        for song_data in SONGS:
            song = Song(
                title=song_data["title"],
                author=authors[song_data["author_idx"]].id,
                description=song_data["description"],
            )
            session.add(song)
            session.flush()

            # Add tags via association table
            for tag_name in song_data["tag_names"]:
                if tag_name in tag_map:
                    session.execute(
                        song_tags.insert().values(
                            song_id=song.id,
                            tag_id=tag_map[tag_name].id,
                        ),
                    )

        session.commit()
        print(f"Seeded {len(TAG_CATEGORIES)} categories, "
              f"{sum(len(v) for v in TAGS_BY_CATEGORY.values())} tags, "
              f"{len(AUTHORS)} authors, {len(SONGS)} songs.")


if __name__ == "__main__":
    seed()
