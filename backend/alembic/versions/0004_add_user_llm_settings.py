"""add user llm settings (bring-your-own-key)

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("llm_provider", sa.String(50), nullable=True))
    op.add_column("users", sa.Column("llm_api_key_encrypted", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("llm_model", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "llm_model")
    op.drop_column("users", "llm_api_key_encrypted")
    op.drop_column("users", "llm_provider")
