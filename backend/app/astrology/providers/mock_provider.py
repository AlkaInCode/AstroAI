"""
Deterministic placeholder provider for local development when no external
astrology API key is configured. It produces stable, clearly-labeled fake
data -- never used in production, and never mistaken for a real calculation
because calculation_provider is recorded as "mock" on every chart.
"""

from app.astrology.provider import AstrologyProvider, BirthInput, ChartResult, PlanetPlacement

_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


class MockAstrologyProvider(AstrologyProvider):
    name = "mock"

    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        seed = birth.dob.toordinal() + int(birth.birth_time.hour) * 60 + int(birth.birth_time.minute)

        planets = []
        for i, planet in enumerate(_PLANETS):
            sign_index = (seed + i * 3) % 12
            house = ((seed + i * 3) % 12) + 1
            degree = round(((seed + i * 7) % 3000) / 100, 2)
            planets.append(
                PlanetPlacement(
                    name=planet,
                    sign=_SIGNS[sign_index],
                    house=house,
                    degree=degree,
                    retrograde=(i in (4, 7)),
                )
            )

        lagna_sign = _SIGNS[seed % 12]

        return ChartResult(
            lagna=lagna_sign,
            rashi=_SIGNS[(seed + 1) % 12],
            ayanamsa="Lahiri",
            house_system="Whole Sign",
            planets=planets,
            raw_response={"provider": "mock", "seed": seed},
        )
