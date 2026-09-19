from pydantic import BaseModel


class VargaPlanetOut(BaseModel):
    name: str
    sign: str
    house: int


class VargaChartResponse(BaseModel):
    key: str
    label: str
    significance: str
    lagna: str
    planets: list[VargaPlanetOut]


class VargaListResponse(BaseModel):
    available: list[dict]
