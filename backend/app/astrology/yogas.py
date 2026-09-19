"""
Deterministic Yoga/Rajyoga detection.

Per the PRD: a rules engine decides whether a Yoga's conditions are met --
the LLM only ever explains a detected Yoga, it never independently decides
whether one exists. Every function here returns plain facts (which Yoga,
which planets, which houses) with no interpretive language; any warm
explanation happens downstream via RAG + the LLM, same as everywhere else
in this app.

Scope: a deliberately bounded, well-known set of classical Yogas with
clear, unambiguous rules -- not an attempt at the hundreds of Yogas found
across classical texts. Each detector is independent and self-contained,
so adding another Yoga later is additive (write one more function, append
it to detect_yogas), never a rewrite of this module.
"""

from app.astrology.derivations import SIGN_RULER, house_lord

_KENDRA_HOUSES = (1, 4, 7, 10)
_TRIKONA_HOUSES = (1, 5, 9)

_MAHAPURUSHA_YOGAS = {
    "Mars": "Ruchaka Yoga",
    "Mercury": "Bhadra Yoga",
    "Jupiter": "Hamsa Yoga",
    "Venus": "Malavya Yoga",
    "Saturn": "Sasa Yoga",
}


def _find_planet(planets: list[dict], name: str) -> dict | None:
    return next((p for p in planets if p["name"] == name), None)


def _is_own_sign(planet: str, sign: str) -> bool:
    return SIGN_RULER.get(sign) == planet


def _relative_house(from_house: int, to_house: int) -> int:
    """The house number of `to_house`, counted from `from_house` as 1st."""
    return ((to_house - from_house) % 12) + 1


def _detect_mahapurusha_yogas(planets: list[dict]) -> list[dict]:
    """Ruchaka/Bhadra/Hamsa/Malavya/Sasa: the planet is in its own sign or
    exalted, AND placed in a kendra (1st/4th/7th/10th) from the Lagna."""
    found = []
    for planet_name, yoga_name in _MAHAPURUSHA_YOGAS.items():
        planet = _find_planet(planets, planet_name)
        if planet is None:
            continue
        if planet["house"] in _KENDRA_HOUSES and (planet["exalted"] or _is_own_sign(planet_name, planet["sign"])):
            found.append(
                {
                    "name": yoga_name,
                    "type": "Pancha Mahapurusha Yoga",
                    "planets": [planet_name],
                    "description": (
                        f"{planet_name} is {'exalted' if planet['exalted'] else 'in its own sign'} "
                        f"({planet['sign']}) while placed in house {planet['house']}, a kendra from the Lagna."
                    ),
                }
            )
    return found


def _detect_gajakesari_yoga(planets: list[dict]) -> list[dict]:
    """Jupiter in a kendra (1st/4th/7th/10th) counted from the Moon's own house."""
    moon = _find_planet(planets, "Moon")
    jupiter = _find_planet(planets, "Jupiter")
    if moon is None or jupiter is None:
        return []
    if _relative_house(moon["house"], jupiter["house"]) in _KENDRA_HOUSES:
        return [
            {
                "name": "Gajakesari Yoga",
                "type": "Chandra Yoga",
                "planets": ["Moon", "Jupiter"],
                "description": (
                    f"Jupiter (house {jupiter['house']}) is in a kendra position counted from the Moon "
                    f"(house {moon['house']})."
                ),
            }
        ]
    return []


def _detect_conjunction_yoga(planets: list[dict], planet_a: str, planet_b: str, name: str, yoga_type: str) -> list[dict]:
    a = _find_planet(planets, planet_a)
    b = _find_planet(planets, planet_b)
    if a is None or b is None or a["house"] != b["house"]:
        return []
    return [
        {
            "name": name,
            "type": yoga_type,
            "planets": [planet_a, planet_b],
            "description": f"{planet_a} and {planet_b} are conjunct together in house {a['house']}.",
        }
    ]


def _detect_raja_yogas(lagna: str, planets: list[dict]) -> list[dict]:
    """A kendra-house lord and a trikona-house lord conjunct in the same house.
    The classical definition of Raja Yoga: an alliance between an 'angle'
    (kendra) and a 'trine' (trikona) lord."""
    kendra_lords = {house: house_lord(lagna, house) for house in _KENDRA_HOUSES}
    trikona_lords = {house: house_lord(lagna, house) for house in _TRIKONA_HOUSES}

    found = []
    seen_pairs = set()
    for kendra_house, kendra_planet in kendra_lords.items():
        for trikona_house, trikona_planet in trikona_lords.items():
            if kendra_planet == trikona_planet:
                continue
            pair_key = frozenset((kendra_planet, trikona_planet))
            if pair_key in seen_pairs:
                continue

            kp = _find_planet(planets, kendra_planet)
            tp = _find_planet(planets, trikona_planet)
            if kp and tp and kp["house"] == tp["house"]:
                seen_pairs.add(pair_key)
                found.append(
                    {
                        "name": "Raja Yoga",
                        "type": "Raja Yoga",
                        "planets": [kendra_planet, trikona_planet],
                        "description": (
                            f"{kendra_planet} (lord of kendra house {kendra_house}) and {trikona_planet} "
                            f"(lord of trikona house {trikona_house}) are conjunct in house {kp['house']}."
                        ),
                    }
                )
    return found


def _detect_dhana_yoga(lagna: str, planets: list[dict]) -> list[dict]:
    """The 2nd lord (accumulated wealth) and 11th lord (gains) conjunct in the same house."""
    second_lord = house_lord(lagna, 2)
    eleventh_lord = house_lord(lagna, 11)
    if second_lord == eleventh_lord:
        return []
    return _detect_conjunction_yoga(planets, second_lord, eleventh_lord, "Dhana Yoga", "Dhana Yoga")


def detect_yogas(lagna: str, planets: list[dict]) -> list[dict]:
    yogas = []
    yogas += _detect_mahapurusha_yogas(planets)
    yogas += _detect_gajakesari_yoga(planets)
    yogas += _detect_conjunction_yoga(planets, "Sun", "Mercury", "Budhaditya Yoga", "Buddhi Yoga")
    yogas += _detect_conjunction_yoga(planets, "Moon", "Mars", "Chandra-Mangal Yoga", "Dhana Yoga")
    yogas += _detect_raja_yogas(lagna, planets)
    yogas += _detect_dhana_yoga(lagna, planets)
    return yogas
