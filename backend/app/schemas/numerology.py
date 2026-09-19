import uuid
from datetime import datetime

from pydantic import BaseModel


class NumerologyNumberOut(BaseModel):
    number: int
    knowledge: str = ""


class NumerologyResponse(BaseModel):
    id: uuid.UUID
    birth_profile_id: uuid.UUID
    full_name_used: str
    life_path: NumerologyNumberOut
    expression: NumerologyNumberOut
    soul_urge: NumerologyNumberOut
    personality: NumerologyNumberOut
    chaldean_destiny: NumerologyNumberOut
    created_at: datetime
