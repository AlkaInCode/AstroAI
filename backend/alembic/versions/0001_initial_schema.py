"""initial schema: users, birth_profiles, charts, conversations

Revision ID: 0001
Revises:
Create Date: 2026-09-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="customer"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "birth_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("gender", sa.String(50), nullable=False),
        sa.Column("dob", sa.Date(), nullable=False),
        sa.Column("birth_time", sa.Time(), nullable=False),
        sa.Column("birth_place", sa.String(255), nullable=False),
        sa.Column("city", sa.String(255), nullable=False),
        sa.Column("state", sa.String(255), nullable=True),
        sa.Column("country", sa.String(255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("timezone", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_birth_profiles_user_id", "birth_profiles", ["user_id"])

    op.create_table(
        "charts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "birth_profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("birth_profiles.id"), nullable=False
        ),
        sa.Column("lagna", sa.String(50), nullable=False),
        sa.Column("rashi", sa.String(50), nullable=False),
        sa.Column("ayanamsa", sa.String(100), nullable=False),
        sa.Column("house_system", sa.String(100), nullable=False),
        sa.Column("calculation_provider", sa.String(100), nullable=False),
        sa.Column("planetary_data", postgresql.JSONB(), nullable=False),
        sa.Column("raw_provider_response", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_charts_birth_profile_id", "charts", ["birth_profile_id"])

    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "birth_profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("birth_profiles.id"), nullable=False
        ),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_conversations_birth_profile_id", "conversations", ["birth_profile_id"])
    op.create_index("ix_conversations_session_id", "conversations", ["session_id"])


def downgrade() -> None:
    op.drop_table("conversations")
    op.drop_table("charts")
    op.drop_table("birth_profiles")
    op.drop_table("users")
