import uuid
from datetime import date, datetime, time

from pydantic import BaseModel, Field


class BirthProfileCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    gender: str = Field(min_length=1, max_length=50)
    dob: date
    birth_time: time
    birth_place: str
    city: str
    state: str | None = None
    country: str
    # Provided by the frontend after the user picks a place from location search.
    latitude: float
    longitude: float
    timezone: str


class BirthProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    gender: str | None = Field(default=None, min_length=1, max_length=50)
    dob: date | None = None
    birth_time: time | None = None
    birth_place: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None


class BirthProfileResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    gender: str
    dob: date
    birth_time: time
    birth_place: str
    city: str
    state: str | None
    country: str
    latitude: float
    longitude: float
    timezone: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
