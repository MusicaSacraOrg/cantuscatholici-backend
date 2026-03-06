"""add lyrics support - song_id on song_order, part_type on song_parts

Revision ID: b7f1a2c3d4e5
Revises: a1b2c3d4e5f6
Create Date: 2026-03-06 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7f1a2c3d4e5"
down_revision: str | Sequence[str] | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add song_id to song_order, part_type to song_parts."""
    op.add_column(
        "song_order",
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id"), nullable=True),
    )
    op.add_column(
        "song_parts",
        sa.Column("part_type", sa.String(), nullable=True),
    )
    op.alter_column("song_parts", "tag_id", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    """Remove lyrics support columns."""
    op.alter_column("song_parts", "tag_id", existing_type=sa.Integer(), nullable=False)
    op.drop_column("song_parts", "part_type")
    op.drop_column("song_order", "song_id")
