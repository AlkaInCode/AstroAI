import uuid
from datetime import datetime

from pydantic import BaseModel


class PlanetPlacement(BaseModel):
    name: str
    sign: str
    house: int
    degree: float
    retrograde: bool = False


class LifeAreaCard(BaseModel):
    title: str
    icon: str
    text: str
    knowledge: str


class ChartResponse(BaseModel):
    id: uuid.UUID
    birth_profile_id: uuid.UUID
    lagna: str
    lagna_degree: float
    rashi: str
    ayanamsa: str
    house_system: str
    calculation_provider: str
    planetary_data: dict
    life_areas: list[LifeAreaCard]
    created_at: datetime

    model_config = {"from_attributes": True}
