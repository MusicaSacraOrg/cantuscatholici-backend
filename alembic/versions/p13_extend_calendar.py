"""extend calendar with date, feast_type, season, calendar_songs m2m

Revision ID: p13a2b3c4d5e
Revises: p12a2b3c4d5e
Create Date: 2026-03-06 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "p13a2b3c4d5e"
down_revision: str | Sequence[str] | None = "p12a2b3c4d5e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Extend calendar_entry and add calendar_songs junction table."""
    op.add_column(
        "calendar_entry",
        sa.Column("date", sa.Date(), nullable=True),
    )
    op.add_column(
        "calendar_entry",
        sa.Column("feast_type", sa.String(), nullable=True),
    )
    op.add_column(
        "calendar_entry",
        sa.Column("liturgical_season", sa.String(), nullable=True),
    )
    op.add_column(
        "calendar_entry",
        sa.Column("is_recurring", sa.Boolean(), server_default="false", nullable=False),
    )
    op.create_table(
        "calendar_songs",
        sa.Column("calendar_entry_id", sa.Integer(), nullable=False),
        sa.Column("song_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["calendar_entry_id"], ["calendar_entry.id"]),
        sa.ForeignKeyConstraint(["song_id"], ["songs.id"]),
        sa.PrimaryKeyConstraint("calendar_entry_id", "song_id"),
    )


def downgrade() -> None:
    """Remove calendar extensions."""
    op.drop_table("calendar_songs")
    op.drop_column("calendar_entry", "is_recurring")
    op.drop_column("calendar_entry", "liturgical_season")
    op.drop_column("calendar_entry", "feast_type")
    op.drop_column("calendar_entry", "date")
