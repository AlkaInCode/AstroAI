"""
Deterministic placeholder provider for local development when no external
astrology API key is configured. It produces stable, clearly-labeled fake
data -- never used in production, and never mistaken for a real calculation
because calculation_provider is recorded as "mock" on every chart.

Sign/house/degree placement is fake, but every Phase-2 attribute derived
from those (Nakshatra, combustion, dignity, Vargottama, aspects) uses the
same real rule engine every provider shares -- see app.astrology.derivations.
"""

import math
from datetime import date

from app.astrology.derivations import SIGNS, absolute_longitude, enrich_planet
from app.astrology.provider import AstrologyProvider, BirthInput, ChartResult, PlanetPlacement, TransitPosition

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# Rough real-world average days-per-sign, used only to make the mock transit
# feed change at a plausible relative pace (Moon fastest, Saturn slowest) --
# not a real ephemeris. Rahu/Ketu move backward through the zodiac.
_TRANSIT_DAYS_PER_SIGN = {
    "Sun": 30.44,
    "Moon": 2.28,
    "Mars": 45,
    "Mercury": 15,
    "Jupiter": 361,
    "Venus": 25,
    "Saturn": 900,
    "Rahu": 547,
    "Ketu": 547,
}
_TRANSIT_START_OFFSET = {"Sun": 0, "Moon": 2, "Mars": 8, "Mercury": 4, "Jupiter": 10, "Venus": 6, "Saturn": 1, "Rahu": 3, "Ketu": 9}
_RETROGRADE_NODES = {"Rahu", "Ketu"}
_TRANSIT_EPOCH = date(2000, 1, 1).toordinal()


class MockAstrologyProvider(AstrologyProvider):
    name = "mock"

    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        seed = birth.dob.toordinal() + int(birth.birth_time.hour) * 60 + int(birth.birth_time.minute)

        raw_placements = []
        for i, planet in enumerate(_PLANETS):
            sign = SIGNS[(seed + i * 3) % 12]
            house = ((seed + i * 3) % 12) + 1
            degree = round(((seed + i * 7) % 3000) / 100, 2)
            raw_placements.append(
                {"name": planet, "sign": sign, "house": house, "degree": degree, "retrograde": i in (4, 7)}
            )

        sun_raw = raw_placements[0]
        sun_longitude = absolute_longitude(sun_raw["sign"], sun_raw["degree"])

        planets = [
            PlanetPlacement(
                name=p["name"],
                sign=p["sign"],
                house=p["house"],
                degree=p["degree"],
                **enrich_planet(p["name"], p["sign"], p["degree"], p["house"], p["retrograde"], sun_longitude),
            )
            for p in raw_placements
        ]

        lagna_sign = SIGNS[seed % 12]
        lagna_degree = round((seed % 3000) / 100, 2)

        return ChartResult(
            lagna=lagna_sign,
            lagna_degree=lagna_degree,
            rashi=SIGNS[(seed + 1) % 12],
            ayanamsa="Lahiri",
            house_system="Whole Sign",
            planets=planets,
            raw_response={"provider": "mock", "seed": seed},
        )

    def calculate_transits(self, as_of: date) -> list[TransitPosition]:
        days_elapsed = as_of.toordinal() - _TRANSIT_EPOCH

        positions = []
        for planet in _PLANETS:
            is_retrograde = planet in _RETROGRADE_NODES
            direction = -1 if is_retrograde else 1
            position = _TRANSIT_START_OFFSET[planet] + direction * days_elapsed / _TRANSIT_DAYS_PER_SIGN[planet]

            sign_offset = math.floor(position)
            degree_fraction = position - sign_offset  # always in [0, 1), regardless of direction

            positions.append(
                TransitPosition(
                    name=planet,
                    sign=SIGNS[sign_offset % 12],
                    degree=round(degree_fraction * 30, 2),
                    retrograde=is_retrograde,
                )
            )
        return positions
