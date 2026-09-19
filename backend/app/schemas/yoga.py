from pydantic import BaseModel


class YogaOut(BaseModel):
    name: str
    type: str
    planets: list[str]
    description: str
    knowledge: str


class YogaListResponse(BaseModel):
    yogas: list[YogaOut]
