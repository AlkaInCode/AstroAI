"""
Resolves a birth place into latitude, longitude and timezone.
Abstracted the same way as the astrology provider: one interface, swappable
implementation, so picking a specific vendor (OpenCage, Google Places, ...)
never leaks into the rest of the app.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.config import settings


@dataclass
class ResolvedLocation:
    latitude: float
    longitude: float
    timezone: str


class GeocodingProvider(ABC):
    @abstractmethod
    def resolve(self, city: str, state: str | None, country: str) -> ResolvedLocation:
        raise NotImplementedError


class MockGeocodingProvider(GeocodingProvider):
    """Deterministic placeholder so Phase 1 can be developed end-to-end before a real key exists."""

    def resolve(self, city: str, state: str | None, country: str) -> ResolvedLocation:
        seed = sum(ord(c) for c in city.lower())
        return ResolvedLocation(
            latitude=round((seed % 180) - 90, 4),
            longitude=round((seed % 360) - 180, 4),
            timezone="UTC",
        )


def get_geocoding_provider() -> GeocodingProvider:
    if settings.geocoding_provider == "mock":
        return MockGeocodingProvider()
    raise NotImplementedError(f"Geocoding provider '{settings.geocoding_provider}' is not implemented yet")
