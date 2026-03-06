from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

song_tags = Table(
    "song_tags",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
