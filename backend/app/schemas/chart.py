import uuid
from datetime import datetime

from pydantic import BaseModel


class PlanetPlacement(BaseModel):
    name: str
    sign: str
    house: int
    degree: float
    retrograde: bool = False


class ChartResponse(BaseModel):
    id: uuid.UUID
    birth_profile_id: uuid.UUID
    lagna: str
    rashi: str
    ayanamsa: str
    house_system: str
    calculation_provider: str
    planetary_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}
