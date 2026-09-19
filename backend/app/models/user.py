import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Reserved for the future astrologer/admin role; every Phase 1 signup is "customer".
    role: Mapped[str] = mapped_column(String(50), default="customer", nullable=False)

    # Bring-your-own-key: lets a user supply their own LLM credentials instead of
    # relying on the server-wide default (see app.ai.llm, app.services.encryption).
    # llm_api_key_encrypted is never decrypted anywhere except at the moment of an
    # actual LLM call, and is never returned to the frontend.
    llm_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    llm_api_key_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    birth_profiles: Mapped[list["BirthProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
