"""
Deterministic placeholder provider for local development when no external
astrology API key is configured. It produces stable, clearly-labeled fake
data -- never used in production, and never mistaken for a real calculation
because calculation_provider is recorded as "mock" on every chart.

Sign/house/degree placement is fake, but every Phase-2 attribute derived
from those (Nakshatra, combustion, dignity, Vargottama, aspects) uses the
same real rule engine every provider shares -- see app.astrology.derivations.
"""

from app.astrology.derivations import SIGNS, absolute_longitude, enrich_planet
from app.astrology.provider import AstrologyProvider, BirthInput, ChartResult, PlanetPlacement

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


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

        return ChartResult(
            lagna=lagna_sign,
            rashi=SIGNS[(seed + 1) % 12],
            ayanamsa="Lahiri",
            house_system="Whole Sign",
            planets=planets,
            raw_response={"provider": "mock", "seed": seed},
        )
