"""
Transit-by-house analysis: combines a provider's current planetary
positions (the same for everyone on a given date) with one customer's
natal Lagna and Moon to determine which of THEIR houses each transiting
planet currently occupies.

Two named, classically well-defined patterns are flagged explicitly since
they're what customers most often ask about:

- Sade Sati: transiting Saturn in the 12th, 1st or 2nd house counted from
  the natal Moon sign (a ~7.5-year period, in three ~2.5-year phases).
- Jupiter Return: transiting Jupiter back in the same sign as natal
  Jupiter (recurs roughly every 12 years).

Both are deterministic rules over real transit + natal facts -- not
predictions, and never invented by the LLM.
"""

from app.astrology.derivations import compute_dignity, sign_index

_SADE_SATI_PHASES = {12: "Rising phase", 1: "Peak phase", 2: "Setting phase"}


def _house_from(reference_sign: str, target_sign: str) -> int:
    return ((sign_index(target_sign) - sign_index(reference_sign)) % 12) + 1


def analyze_transits(
    transit_positions: list[dict],
    natal_lagna: str,
    natal_moon_sign: str,
    natal_planets: list[dict],
) -> dict:
    transits = []
    for t in transit_positions:
        exalted, debilitated = compute_dignity(t["name"], t["sign"])
        transits.append(
            {
                "name": t["name"],
                "sign": t["sign"],
                "degree": t["degree"],
                "retrograde": t["retrograde"],
                "house_from_lagna": _house_from(natal_lagna, t["sign"]),
                "house_from_moon": _house_from(natal_moon_sign, t["sign"]),
                "exalted": exalted,
                "debilitated": debilitated,
            }
        )

    saturn_transit = next((t for t in transits if t["name"] == "Saturn"), None)
    sade_sati_house = saturn_transit["house_from_moon"] if saturn_transit else None
    sade_sati = {
        "active": sade_sati_house in _SADE_SATI_PHASES,
        "phase": _SADE_SATI_PHASES.get(sade_sati_house),
    }

    natal_jupiter = next((p for p in natal_planets if p["name"] == "Jupiter"), None)
    transit_jupiter = next((t for t in transits if t["name"] == "Jupiter"), None)
    jupiter_return = bool(natal_jupiter and transit_jupiter and natal_jupiter["sign"] == transit_jupiter["sign"])

    return {
        "transits": transits,
        "sade_sati": sade_sati,
        "jupiter_return": jupiter_return,
    }
