"""
Phase 3 "Better Personal Analysis": Personality, Career, Love, Money and
General life-theme summaries.

Still deterministic and template-based -- no LLM call -- but now reasons
over house lords and each significator's actual dignity/combustion/
Vargottama state (the Phase 2 attributes), and cites a short RAG-retrieved
passage per card, the same knowledge base the AI chat draws from. This is
the "stronger chart-aware reasoning + RAG" step the PRD calls for, without
requiring an LLM key -- when one is added later, this module's inputs
(chart facts + retrieved knowledge) are exactly what a real LLM call would
also need, so the upgrade path is additive, not a rewrite.
"""

from app.ai.rag import search_astrology_knowledge
from app.astrology.derivations import house_lord, house_sign

SIGN_TRAITS = {
    "Aries": "bold, direct and quick to act",
    "Taurus": "steady, patient and grounded",
    "Gemini": "curious, adaptable and communicative",
    "Cancer": "sensitive, nurturing and intuitive",
    "Leo": "confident, warm and expressive",
    "Virgo": "detail-oriented, practical and thoughtful",
    "Libra": "diplomatic, balanced and relationship-focused",
    "Scorpio": "intense, resilient and perceptive",
    "Sagittarius": "optimistic, adventurous and philosophical",
    "Capricorn": "disciplined, ambitious and responsible",
    "Aquarius": "independent, original and idealistic",
    "Pisces": "imaginative, compassionate and dreamy",
}


def _find_planet(planets: list[dict], name: str) -> dict | None:
    return next((p for p in planets if p["name"] == name), None)


def _describe_state(planet: dict | None) -> str:
    if planet is None:
        return "not placed in this chart"
    tags = []
    if planet["exalted"]:
        tags.append("exalted")
    if planet["debilitated"]:
        tags.append("debilitated")
    if planet["combust"]:
        tags.append("combust")
    if planet["vargottama"]:
        tags.append("Vargottama")
    if planet["retrograde"]:
        tags.append("retrograde")
    state = f" ({', '.join(tags)})" if tags else ""
    return f"in {planet['sign']} in house {planet['house']}{state}"


def _occupants_of(planets: list[dict], house: int) -> list[dict]:
    return [p for p in planets if p["house"] == house]


def _names(planets: list[dict]) -> str:
    names = [p["name"] for p in planets]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{', '.join(names[:-1])} and {names[-1]}"


def _knowledge_note(query: str) -> str:
    results = search_astrology_knowledge(query, top_k=1, allow_fallback=False)
    return results[0]["content"] if results else ""


def _build_money_text(lagna: str, second_lord: dict | None, eleventh_lord: dict | None, jupiter: dict | None) -> str:
    second_lord_name = house_lord(lagna, 2)
    eleventh_lord_name = house_lord(lagna, 11)

    if second_lord_name == eleventh_lord_name:
        # Common for several Lagnas: e.g. Aquarius rising puts both the 2nd (Pisces)
        # and 11th (Sagittarius) houses under Jupiter's rulership.
        lords_sentence = (
            f"Both your 2nd house of accumulated wealth and 11th house of gains are ruled by "
            f"{second_lord_name}, who is {_describe_state(second_lord)}."
        )
    else:
        lords_sentence = (
            f"Your 2nd house of accumulated wealth is ruled by {second_lord_name}, who is "
            f"{_describe_state(second_lord)}, while your 11th house of gains is ruled by "
            f"{eleventh_lord_name}, {_describe_state(eleventh_lord)}."
        )

    if jupiter and jupiter["name"] in (second_lord_name, eleventh_lord_name):
        jupiter_sentence = "As the natural significator of abundance, Jupiter's own condition here carries extra weight."
    else:
        jupiter_sentence = f"Jupiter, the significator of abundance, is {_describe_state(jupiter)}."

    return f"{lords_sentence} {jupiter_sentence}"


def build_life_areas(lagna: str, rashi: str, planets: list[dict]) -> list[dict]:
    lagna_lord_name = house_lord(lagna, 1)
    lagna_lord = _find_planet(planets, lagna_lord_name)
    moon = _find_planet(planets, "Moon")
    venus = _find_planet(planets, "Venus")
    jupiter = _find_planet(planets, "Jupiter")

    tenth_sign = house_sign(lagna, 10)
    tenth_lord = _find_planet(planets, house_lord(lagna, 10))
    seventh_lord = _find_planet(planets, house_lord(lagna, 7))
    second_lord = _find_planet(planets, house_lord(lagna, 2))
    eleventh_lord = _find_planet(planets, house_lord(lagna, 11))

    vargottama_planets = _names([p for p in planets if p["vargottama"]])

    return [
        {
            "title": "Personality",
            "icon": "🌟",
            "text": (
                f"With {lagna} rising and a {rashi} Moon, your natural temperament leans "
                f"{SIGN_TRAITS.get(lagna, lagna)} with a {SIGN_TRAITS.get(rashi, rashi)} emotional undercurrent. "
                f"Your Lagna lord {lagna_lord_name} sits {_describe_state(lagna_lord)}, which colors how strongly "
                f"that core temperament comes through day to day."
            ),
            "knowledge": _knowledge_note(lagna_lord_name),
        },
        {
            "title": "Career",
            "icon": "💼",
            "text": (
                f"Your 10th house of career falls in {tenth_sign}, ruled by {house_lord(lagna, 10)}, who is "
                f"{_describe_state(tenth_lord)}."
                + (
                    f" {_names(_occupants_of(planets, 10))} placed directly in the 10th house adds further weight "
                    f"to how you show up professionally."
                    if _occupants_of(planets, 10)
                    else " No planets sit directly in the 10th house, so career themes run mainly through this house lord."
                )
            ),
            "knowledge": _knowledge_note("career " + house_lord(lagna, 10)),
        },
        {
            "title": "Love & Relationships",
            "icon": "💗",
            "text": (
                f"Your 7th house of partnership is ruled by {house_lord(lagna, 7)}, who is "
                f"{_describe_state(seventh_lord)}. Venus, the natural significator of love, is "
                f"{_describe_state(venus)}."
                + (
                    f" {_names(_occupants_of(planets, 7))} in the 7th house directly shapes your approach to commitment."
                    if _occupants_of(planets, 7)
                    else ""
                )
            ),
            "knowledge": _knowledge_note("seventh house Venus"),
        },
        {
            "title": "Money",
            "icon": "💰",
            "text": _build_money_text(lagna, second_lord, eleventh_lord, jupiter),
            "knowledge": _knowledge_note("wealth Jupiter"),
        },
        {
            "title": "General Life Themes",
            "icon": "🧭",
            "text": (
                f"Your chart's overall tone is set by your {lagna} Lagna and its lord {lagna_lord_name}, "
                f"{_describe_state(lagna_lord)}."
                + (
                    f" {vargottama_planets} in Vargottama placement adds notable strength to whatever "
                    f"{'that planet' if ' and ' not in vargottama_planets and ',' not in vargottama_planets else 'those planets'} signify."
                    if vargottama_planets
                    else " No planet is Vargottama in this chart, so no single placement is unusually reinforced this way."
                )
            ),
            "knowledge": _knowledge_note("Lagna"),
        },
    ]
