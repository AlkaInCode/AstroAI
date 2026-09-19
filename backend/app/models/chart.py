import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Chart(Base):
    __tablename__ = "charts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    birth_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("birth_profiles.id"), nullable=False, index=True
    )

    lagna: Mapped[str] = mapped_column(String(50), nullable=False)
    rashi: Mapped[str] = mapped_column(String(50), nullable=False)
    ayanamsa: Mapped[str] = mapped_column(String(100), nullable=False)
    house_system: Mapped[str] = mapped_column(String(100), nullable=False)
    calculation_provider: Mapped[str] = mapped_column(String(100), nullable=False)

    # Structured, normalized chart facts our own tools/UI read from. Shape:
    # {"planets": [{"name": "Jupiter", "sign": "Leo", "house": 5, "degree": 12.34, "retrograde": false}, ...]}
    planetary_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Untouched provider response, kept so a chart can be reprocessed later without re-calling the API.
    raw_provider_response: Mapped[dict] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    birth_profile: Mapped["BirthProfile"] = relationship(back_populates="charts")
