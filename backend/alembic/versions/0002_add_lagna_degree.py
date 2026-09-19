"""add lagna_degree to charts

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("charts", sa.Column("lagna_degree", sa.Float(), nullable=False, server_default="0"))
    op.alter_column("charts", "lagna_degree", server_default=None)


def downgrade() -> None:
    op.drop_column("charts", "lagna_degree")
