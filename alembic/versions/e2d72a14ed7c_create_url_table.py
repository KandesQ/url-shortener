"""Create url table

Revision ID: e2d72a14ed7c
Revises: 
Create Date: 2026-03-06 04:21:39.485654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2d72a14ed7c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "urls",
        sa.Column("id", sa.BigInteger(), nullable=False, primary_key=True),
        sa.Column("short_identifier", sa.String(length=10), nullable=False, unique=True),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.Column("click_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("urls")
