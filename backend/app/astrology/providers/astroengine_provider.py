"""
AstroEngine integration -- a self-hosted Vedic astrology calculation service
(https://github.com/thebrownhuman/AstroEngine) that exposes chart/yoga/
transit endpoints built to closely mirror Prokerala's data, with no API key
required. Used as a stand-in until (or instead of) a paid Prokerala account.
"""

from datetime import date

import httpx

from app.astrology.derivations import enrich_planet
from app.astrology.provider import AstrologyProvider, BirthInput, ChartResult, PlanetPlacement, TransitPosition
from app.config import settings

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


class AstroEngineProvider(AstrologyProvider):
    name = "astroengine"

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = (base_url or settings.astroengine_base_url).rstrip("/")

    def _post(self, path: str, payload: dict) -> dict:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(f"{self._base_url}{path}", json=payload)
            response.raise_for_status()
            return response.json()

    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        payload = self._post(
            "/v1/chart",
            {
                "date": birth.dob.isoformat(),
                "time": birth.birth_time.strftime("%H:%M:%S"),
                "latitude": birth.latitude,
                "longitude": birth.longitude,
                "timezone": birth.timezone,
            },
        )
        return self._map_chart_response(payload)

    @staticmethod
    def _map_chart_response(payload: dict) -> ChartResult:
        grahas = payload["grahas"]
        sun_longitude = grahas["Sun"]["longitude"]

        planets = [
            PlanetPlacement(
                name=name,
                sign=data["sign_en"],
                house=data["house"],
                degree=data["degree_in_sign"],
                **enrich_planet(
                    name,
                    data["sign_en"],
                    data["degree_in_sign"],
                    data["house"],
                    data["retrograde"],
                    sun_longitude,
                ),
            )
            for name, data in grahas.items()
            if name in _PLANETS
        ]

        lagna = payload["lagna"]
        engine = payload["engine"]

        return ChartResult(
            lagna=lagna["sign_en"],
            lagna_degree=lagna["degree_in_sign"],
            rashi=grahas["Moon"]["sign_en"],
            ayanamsa=engine["ayanamsa"].replace("_", " ").title(),
            house_system=engine["house_convention"].replace("_", " ").title(),
            planets=planets,
            raw_response=payload,
        )

    def calculate_transits(self, as_of: date) -> list[TransitPosition]:
        # Transits are the same for everyone on a given date, independent of any
        # individual's birth chart -- a fixed reference place/time is only needed
        # because AstroEngine's chart endpoint requires a location, but only the
        # planets' sign/degree (never the house, which this call never reads) is used.
        payload = self._post(
            "/v1/chart",
            {"date": as_of.isoformat(), "time": "12:00:00", "place": "Delhi", "timezone": "Asia/Kolkata"},
        )
        grahas = payload["grahas"]
        return [
            TransitPosition(
                name=name,
                sign=data["sign_en"],
                degree=data["degree_in_sign"],
                retrograde=data["retrograde"],
            )
            for name, data in grahas.items()
            if name in _PLANETS
        ]
