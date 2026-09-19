from pydantic import BaseModel


class TransitPlanetOut(BaseModel):
    name: str
    sign: str
    degree: float
    retrograde: bool
    house_from_lagna: int
    house_from_moon: int
    exalted: bool
    debilitated: bool
    knowledge: str = ""


class SadeSatiOut(BaseModel):
    active: bool
    phase: str | None


class TransitResponse(BaseModel):
    as_of: str
    transits: list[TransitPlanetOut]
    sade_sati: SadeSatiOut
    jupiter_return: bool
