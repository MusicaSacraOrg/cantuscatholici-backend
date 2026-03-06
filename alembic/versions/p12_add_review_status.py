"""add review status and review_id to comments

Revision ID: p12a2b3c4d5e
Revises: p11a2b3c4d5e
Create Date: 2026-03-06 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "p12a2b3c4d5e"
down_revision: str | Sequence[str] | None = "p11a2b3c4d5e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add status to song_mr, review_id to review_comments."""
    op.add_column(
        "song_mr",
        sa.Column("status", sa.String(), server_default="open", nullable=False),
    )
    op.add_column(
        "review_comments",
        sa.Column(
            "review_id",
            sa.Integer(),
            sa.ForeignKey("song_mr.id"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove added columns."""
    op.drop_column("review_comments", "review_id")
    op.drop_column("song_mr", "status")
