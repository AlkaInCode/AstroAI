from app.astrology.provider import AstrologyProvider
from app.astrology.providers.mock_provider import MockAstrologyProvider
from app.astrology.providers.prokerala_provider import ProkeralaAstrologyProvider
from app.config import settings


def get_astrology_provider() -> AstrologyProvider:
    if settings.astrology_provider == "prokerala":
        return ProkeralaAstrologyProvider()
    return MockAstrologyProvider()
