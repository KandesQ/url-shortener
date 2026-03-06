"""Url table versioning

Revision ID: 9be8778d7d14
Revises: e2d72a14ed7c
Create Date: 2026-03-07 16:52:44.502065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9be8778d7d14'
down_revision: Union[str, Sequence[str], None] = 'e2d72a14ed7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "urls",
        sa.Column("version_id", sa.Integer, server_default="1", nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("urls", "version_id")