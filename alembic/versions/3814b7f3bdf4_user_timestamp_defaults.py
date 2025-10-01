"""user_timestamp_defaults

Revision ID: 3814b7f3bdf4
Revises: 6e81b0b10235
Create Date: 2025-10-01 22:32:31.522103

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3814b7f3bdf4"
down_revision: str | Sequence[str] | None = "6e81b0b10235"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "registered_at", server_default="NOW")
    op.alter_column("user_content", "added_at", server_default="NOW")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "registered_at", server_default=None)
    op.alter_column("user_content", "added_at", server_default=None)
