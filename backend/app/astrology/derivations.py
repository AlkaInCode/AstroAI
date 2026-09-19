"""
Phase 2 planetary-state derivations: Nakshatra/Pada, combustion, exaltation/
debilitation, Vargottama, and Parashari aspects.

These are deterministic rule engines, not guesses -- given whatever raw sign/
degree/house a calculation provider returns, the rules here are the same
classical Vedic conventions any provider would apply. Keeping them here (
provider-agnostic) means every provider gets these attributes even if it
doesn't return them directly itself.

Vargottama needs a Navamsa (D9) sign for comparison. Rather than wait for
the full divisional-chart infrastructure (PRD Phase 6), a minimal Navamsa
sign calculation is included here -- used only to derive the Vargottama
flag, not to expose a general D9 chart.
"""

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
_NAKSHATRA_SPAN = 360 / 27  # 13deg20'
_PADA_SPAN = _NAKSHATRA_SPAN / 4  # 3deg20'

# Exaltation/debilitation signs are always exactly opposite each other.
# Rahu/Ketu exaltation varies by text; Gemini/Sagittarius is the more
# commonly cited modern convention and is used here.
_EXALTATION_SIGN = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
    "Rahu": "Gemini",
    "Ketu": "Sagittarius",
}

_MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
_FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
# Dual/mutable signs are the remaining four (Gemini, Virgo, Sagittarius, Pisces).

# Classical combustion orbs (degrees from the Sun) by planet.
_COMBUSTION_ORB = {
    "Moon": 12,
    "Mars": 17,
    "Mercury": 14,
    "Jupiter": 11,
    "Venus": 10,
    "Saturn": 15,
}

# Parashari special aspects, given as the traditional house-count labels
# (every planet also casts the universal 7th-house aspect; these are each
# planet's additional ones). A "4th house aspect" from house H lands on
# H+3, not H+4 -- counting starts at H itself as the 1st house.
_SPECIAL_ASPECTS = {
    "Mars": (4, 8),
    "Jupiter": (5, 9),
    "Saturn": (3, 10),
}


def sign_index(sign: str) -> int:
    return SIGNS.index(sign)


def absolute_longitude(sign: str, degree_in_sign: float) -> float:
    return sign_index(sign) * 30 + degree_in_sign


_EPSILON = 1e-9  # guards against float division landing just under an exact boundary


def compute_nakshatra(longitude: float) -> tuple[str, int]:
    longitude = longitude % 360
    nakshatra_index = int((longitude + _EPSILON) // _NAKSHATRA_SPAN)
    position_in_nakshatra = longitude - nakshatra_index * _NAKSHATRA_SPAN
    pada = int((position_in_nakshatra + _EPSILON) // _PADA_SPAN) + 1
    return NAKSHATRAS[nakshatra_index], pada


def compute_dignity(planet: str, sign: str) -> tuple[bool, bool]:
    """Returns (exalted, debilitated)."""
    exaltation_sign = _EXALTATION_SIGN.get(planet)
    if exaltation_sign is None:
        return False, False
    debilitation_sign = SIGNS[(sign_index(exaltation_sign) + 6) % 12]
    return sign == exaltation_sign, sign == debilitation_sign


def compute_combust(planet: str, planet_longitude: float, sun_longitude: float) -> bool:
    orb = _COMBUSTION_ORB.get(planet)
    if orb is None:
        return False
    separation = abs(planet_longitude - sun_longitude) % 360
    separation = min(separation, 360 - separation)
    return separation <= orb


def compute_navamsa_sign(sign: str, degree_in_sign: float) -> str:
    navamsa_index = int((degree_in_sign + _EPSILON) // (30 / 9))
    if sign in _MOVABLE_SIGNS:
        start_offset = 0
    elif sign in _FIXED_SIGNS:
        start_offset = 8  # 9th sign from itself
    else:
        start_offset = 4  # 5th sign from itself
    start = (sign_index(sign) + start_offset) % 12
    return SIGNS[(start + navamsa_index) % 12]


def compute_vargottama(sign: str, degree_in_sign: float) -> bool:
    return compute_navamsa_sign(sign, degree_in_sign) == sign


def compute_aspected_houses(planet: str, house: int) -> list[int]:
    """Houses this planet casts a Parashari aspect on, counting its own house as 1."""
    house_labels = (7,) + _SPECIAL_ASPECTS.get(planet, ())
    return sorted({((house - 1 + (label - 1)) % 12) + 1 for label in house_labels})


# Rahu/Ketu are shadow points that are always treated as retrograde.
_ALWAYS_RETROGRADE = {"Rahu", "Ketu"}


def enrich_planet(
    name: str,
    sign: str,
    degree_in_sign: float,
    house: int,
    base_retrograde: bool,
    sun_longitude: float,
) -> dict:
    """Computes every Phase-2 derived attribute for one planet placement.

    Shared by every AstrologyProvider so these attributes are consistent
    regardless of which provider supplied the raw sign/degree/house.
    """
    longitude = absolute_longitude(sign, degree_in_sign)
    nakshatra, pada = compute_nakshatra(longitude)
    exalted, debilitated = compute_dignity(name, sign)

    return {
        "retrograde": True if name in _ALWAYS_RETROGRADE else base_retrograde,
        "nakshatra": nakshatra,
        "nakshatra_pada": pada,
        "exalted": exalted,
        "debilitated": debilitated,
        "combust": compute_combust(name, longitude, sun_longitude),
        "vargottama": compute_vargottama(sign, degree_in_sign),
        "aspects": compute_aspected_houses(name, house),
    }
