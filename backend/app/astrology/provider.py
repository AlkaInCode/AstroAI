"""
The astrology calculation provider boundary.

Every external astrology API/engine must implement AstrologyProvider so the
rest of the app never depends on a specific vendor's request/response shape.
Swapping providers, or adding a second one for cross-validation, means adding
one new implementation here -- nothing else in the app changes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
    nakshatra: str = ""
    nakshatra_pada: int = 0
    exalted: bool = False
    debilitated: bool = False
    combust: bool = False
    vargottama: bool = False
    aspects: list[int] = field(default_factory=list)


@dataclass
class ChartResult:
    lagna: str
    lagna_degree: float
    rashi: str
    ayanamsa: str
    house_system: str
    planets: list[PlanetPlacement]
    raw_response: dict


@dataclass
class TransitPosition:
    """A planet's current sign/degree, independent of any individual's birth
    chart -- transits are the same for everyone on a given date. Combining
    this with a natal chart (house-from-Lagna, house-from-Moon, etc.) is
    app.astrology.transits' job, not the provider's."""

    name: str
    sign: str
    degree: float
    retrograde: bool = False


class AstrologyProvider(ABC):
    """Facts only. Never guessed, never hardcoded."""

    name: str

    @abstractmethod
    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        raise NotImplementedError

    @abstractmethod
    def calculate_transits(self, as_of: date) -> list[TransitPosition]:
        raise NotImplementedError
