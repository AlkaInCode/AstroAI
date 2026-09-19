"""
Tools the AI agent is allowed to call for chart-specific facts.

Every tool here returns real, stored data -- the agent must call one of
these for any question about the customer's chart. It must never answer
a chart-fact question from the LLM's own "knowledge". Phase 1 covers
profile/chart/planets/houses; Phase 2 adds get_nakshatra (planet
placements now carry Nakshatra, Pada, combustion, dignity, Vargottama
and aspects -- see app.astrology.derivations). get_dasha/get_yogas/
get_transits remain stubbed for Phases 4/5/7.
"""

import uuid

from sqlalchemy.orm import Session

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


def get_dasha(db: Session, birth_profile_id: uuid.UUID) -> dict:
    return {"error": "not_implemented", "detail": "Dasha data arrives in Phase 4"}


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
