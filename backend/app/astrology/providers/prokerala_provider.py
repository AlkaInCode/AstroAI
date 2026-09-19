"""
Prokerala Astrology API integration (primary provider per the PRD).

Prokerala uses OAuth2 client-credentials for auth and exposes Kundli /
birth-chart endpoints that return Lagna, Rashi and planetary positions.
Endpoint paths and response fields must be confirmed against Prokerala's
current API docs before this goes live -- this class is the single place
that mapping lives, so the rest of the app is unaffected by that work.
"""

import httpx

from app.astrology.derivations import absolute_longitude, enrich_planet
from app.astrology.provider import AstrologyProvider, BirthInput, ChartResult, PlanetPlacement
from app.config import settings

_TOKEN_URL = "https://api.prokerala.com/token"
_KUNDLI_URL = "https://api.prokerala.com/v2/astrology/kundli"


class ProkeralaAstrologyProvider(AstrologyProvider):
    name = "prokerala"

    def __init__(self, client_id: str | None = None, client_secret: str | None = None) -> None:
        self._client_id = client_id or settings.prokerala_client_id
        self._client_secret = client_secret or settings.prokerala_client_secret

    def _get_access_token(self, client: httpx.Client) -> str:
        response = client.post(
            _TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def calculate_chart(self, birth: BirthInput) -> ChartResult:
        with httpx.Client(timeout=15.0) as client:
            token = self._get_access_token(client)
            response = client.get(
                _KUNDLI_URL,
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "ayanamsa": 1,  # Lahiri
                    "coordinates": f"{birth.latitude},{birth.longitude}",
                    "datetime": f"{birth.dob.isoformat()}T{birth.birth_time.isoformat()}{_tz_offset(birth.timezone)}",
                },
            )
            response.raise_for_status()
            payload = response.json()

        return self._map_response(payload)

    @staticmethod
    def _map_response(payload: dict) -> ChartResult:
        data = payload.get("data", {})
        raw_positions = data.get("planet_position", [])

        sun_raw = next((p for p in raw_positions if p["name"] == "Sun"), None)
        sun_longitude = absolute_longitude(sun_raw["rasi"]["name"], sun_raw["longitude"]) if sun_raw else 0.0

        planets = [
            PlanetPlacement(
                name=p["name"],
                sign=p["rasi"]["name"],
                house=p["position"],
                degree=p["longitude"],
                **enrich_planet(
                    p["name"], p["rasi"]["name"], p["longitude"], p["position"],
                    p.get("is_retrograde", False), sun_longitude,
                ),
            )
            for p in raw_positions
        ]
        return ChartResult(
            lagna=data.get("ascendant", {}).get("name", ""),
            # TODO: confirm the actual field name for the Ascendant's degree-within-sign
            # against Prokerala's live docs once credentials exist; this key is a guess.
            lagna_degree=data.get("ascendant", {}).get("longitude", 0.0),
            rashi=data.get("chandra_rasi", {}).get("name", ""),
            ayanamsa="Lahiri",
            house_system="Whole Sign",
            planets=planets,
            raw_response=payload,
        )


def _tz_offset(timezone_name: str) -> str:
    """Placeholder: resolve an IANA timezone name to a +HH:MM offset for the given date/time."""
    return "+00:00"
