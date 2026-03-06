"""add song_id to user_content

Revision ID: p11a2b3c4d5e
Revises: b7f1a2c3d4e5
Create Date: 2026-03-06 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "p11a2b3c4d5e"
down_revision: str | Sequence[str] | None = "b7f1a2c3d4e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add song_id and content_type to user_content."""
    op.add_column(
        "user_content",
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id"), nullable=True),
    )
    op.add_column(
        "user_content",
        sa.Column("content_type", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Remove song_id and content_type from user_content."""
    op.drop_column("user_content", "content_type")
    op.drop_column("user_content", "song_id")
