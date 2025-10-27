"""add refresh tokens table

Revision ID: add_refresh_tokens
Revises: 7acb1f0aa6e5
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "add_refresh_tokens"
down_revision: str | Sequence[str] | None = "7acb1f0aa6e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(
                timezone=True),
            nullable=False,
            server_default=sa.func.now()),
        sa.Column(
            "is_revoked",
            sa.Boolean(),
            nullable=False,
            server_default="false"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        "ix_refresh_tokens_token",
        "refresh_tokens",
        ["token"],
        unique=True)
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_token", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
