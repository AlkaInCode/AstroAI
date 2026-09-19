"""
Tools the AI agent is allowed to call for chart-specific facts.

Every tool here returns real, stored data -- the agent must call one of
these for any question about the customer's chart. It must never answer
a chart-fact question from the LLM's own "knowledge". Phase 1 covers
profile/chart/planets/houses; Phase 2 adds get_nakshatra (planet
placements now carry Nakshatra, Pada, combustion, dignity, Vargottama
and aspects -- see app.astrology.derivations). Phase 4 adds get_dasha
(Vimshottari Mahadasha/Antardasha/Pratyantardasha -- see
app.astrology.dasha). get_yogas/get_transits remain stubbed for Phases 5/7.
"""

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.astrology.dasha import compute_dasha
from app.astrology.derivations import absolute_longitude
from app.models.birth_profile import BirthProfile
from app.models.chart import Chart


def get_profile(db: Session, birth_profile_id: uuid.UUID) -> dict:
    profile = db.get(BirthProfile, birth_profile_id)
    if profile is None:
        return {"error": "profile_not_found"}
    return {
        "full_name": profile.full_name,
        "gender": profile.gender,
        "dob": profile.dob.isoformat(),
        "birth_time": profile.birth_time.isoformat(),
        "birth_place": profile.birth_place,
        "city": profile.city,
        "country": profile.country,
    }


def get_chart(db: Session, birth_profile_id: uuid.UUID) -> dict:
    chart = (
        db.query(Chart)
        .filter(Chart.birth_profile_id == birth_profile_id)
        .order_by(Chart.created_at.desc())
        .first()
    )
    if chart is None:
        return {"error": "chart_not_found"}
    return {
        "lagna": chart.lagna,
        "rashi": chart.rashi,
        "ayanamsa": chart.ayanamsa,
        "house_system": chart.house_system,
        "planets": chart.planetary_data.get("planets", []),
    }


def get_planet_details(db: Session, birth_profile_id: uuid.UUID, planet_name: str) -> dict:
    chart_data = get_chart(db, birth_profile_id)
    if "error" in chart_data:
        return chart_data
    for planet in chart_data["planets"]:
        if planet["name"].lower() == planet_name.lower():
            return planet
    return {"error": "planet_not_found", "planet": planet_name}


def get_house_details(db: Session, birth_profile_id: uuid.UUID, house_number: int) -> dict:
    chart_data = get_chart(db, birth_profile_id)
    if "error" in chart_data:
        return chart_data
    occupants = [p for p in chart_data["planets"] if p["house"] == house_number]
    aspected_by = [p["name"] for p in chart_data["planets"] if house_number in p.get("aspects", [])]
    return {"house": house_number, "occupants": occupants, "aspected_by": aspected_by}


def get_nakshatra(db: Session, birth_profile_id: uuid.UUID, planet_name: str) -> dict:
    planet = get_planet_details(db, birth_profile_id, planet_name)
    if "error" in planet:
        return planet
    return {
        "planet": planet["name"],
        "nakshatra": planet["nakshatra"],
        "pada": planet["nakshatra_pada"],
    }


def compute_dasha_for_profile(db: Session, birth_profile_id: uuid.UUID, as_of: date | None = None) -> dict:
    """Shared by the AI tool (trimmed) and the /dasha API route (full detail)."""
    profile = db.get(BirthProfile, birth_profile_id)
    if profile is None:
        return {"error": "profile_not_found"}

    chart_data = get_chart(db, birth_profile_id)
    if "error" in chart_data:
        return chart_data

    moon = next((p for p in chart_data["planets"] if p["name"] == "Moon"), None)
    if moon is None:
        return {"error": "moon_position_unavailable"}

    moon_longitude = absolute_longitude(moon["sign"], moon["degree"])
    return compute_dasha(profile.dob, moon_longitude, as_of=as_of)


def get_dasha(db: Session, birth_profile_id: uuid.UUID) -> dict:
    result = compute_dasha_for_profile(db, birth_profile_id)
    if "error" in result:
        return result
    # Trimmed for AI grounding -- the full 9-Mahadasha/81-Antardasha tree is
    # for the dashboard timeline (GET /profiles/{id}/dasha), not chat context.
    return {
        "current_mahadasha": result["current_mahadasha"],
        "current_antardasha": result["current_antardasha"],
        "current_pratyantardasha": result["current_pratyantardasha"],
        "upcoming_mahadashas": [
            {"planet": m["planet"], "start": m["start"], "end": m["end"]}
            for m in result["mahadasha_sequence"]
            if m["start"] > date.today().isoformat()
        ][:3],
    }


def get_yogas(db: Session, birth_profile_id: uuid.UUID) -> dict:
    return {"error": "not_implemented", "detail": "Yoga detection arrives in Phase 5"}


def get_transits(db: Session, birth_profile_id: uuid.UUID) -> dict:
    return {"error": "not_implemented", "detail": "Transit data arrives in Phase 7"}


TOOL_REGISTRY = {
    "get_profile": get_profile,
    "get_chart": get_chart,
    "get_planet_details": get_planet_details,
    "get_house_details": get_house_details,
    "get_nakshatra": get_nakshatra,
    "get_dasha": get_dasha,
    "get_yogas": get_yogas,
    "get_transits": get_transits,
}
