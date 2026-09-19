"""add numerology_results table

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "numerology_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "birth_profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("birth_profiles.id"), nullable=False
        ),
        sa.Column("full_name_used", sa.String(255), nullable=False),
        sa.Column("life_path_number", sa.Integer(), nullable=False),
        sa.Column("expression_number", sa.Integer(), nullable=False),
        sa.Column("soul_urge_number", sa.Integer(), nullable=False),
        sa.Column("personality_number", sa.Integer(), nullable=False),
        sa.Column("chaldean_destiny_number", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_numerology_results_birth_profile_id", "numerology_results", ["birth_profile_id"])


def downgrade() -> None:
    op.drop_table("numerology_results")
