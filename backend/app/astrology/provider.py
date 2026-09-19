"""
The astrology calculation provider boundary.

Every external astrology API/engine must implement AstrologyProvider so the
rest of the app never depends on a specific vendor's request/response shape.
Swapping providers, or adding a second one for cross-validation, means adding
one new implementation here -- nothing else in the app changes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, time


@dataclass
class BirthInput:
    dob: date
    birth_time: time
    latitude: float
    longitude: float
    timezone: str


@dataclass
class PlanetPlacement:
    name: str
    sign: str
    house: int
    degree: float
    retrograde: bool = False


@dataclass
class ChartResult:
    lagna: str
    rashi: str
    ayanamsa: str
    house_system: str
    planets: list[PlanetPlacement]
    raw_response: dict


class AstrologyProvider(ABC):
    """Facts only. Never guessed, never hardcoded."""

    name: str

    @abstractmethod
    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        raise NotImplementedError
