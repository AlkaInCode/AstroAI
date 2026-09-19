import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class NumerologyResult(Base):
    __tablename__ = "numerology_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    birth_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("birth_profiles.id"), nullable=False, index=True
    )

    # The exact name string the calculation used, since numerology is name-sensitive
    # (a legal-name change would change these numbers) -- kept alongside the profile's
    # current full_name so a past result stays explainable even if the name is edited later.
    full_name_used: Mapped[str] = mapped_column(String(255), nullable=False)

    life_path_number: Mapped[int] = mapped_column(Integer, nullable=False)
    expression_number: Mapped[int] = mapped_column(Integer, nullable=False)
    soul_urge_number: Mapped[int] = mapped_column(Integer, nullable=False)
    personality_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chaldean_destiny_number: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    birth_profile: Mapped["BirthProfile"] = relationship(back_populates="numerology_results")
