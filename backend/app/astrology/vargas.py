"""
Reusable divisional chart (Varga) infrastructure.

Per the PRD: build reusable chart infrastructure instead of a separate
hard-coded implementation per divisional chart. Every Varga here is just a
sign/degree -> sign function, computed by the same generic formula
(divide the sign into N equal parts, starting from whichever sign the
classical counting rule for that Varga dictates). Adding another Varga
later means registering one more definition -- see VARGA_REGISTRY --
never writing a new calculator.

D9 (Navamsa) reuses app.astrology.derivations.compute_navamsa_sign
directly, since that Phase-2 code already implements and tests exactly
this formula for a single planet (needed there to derive Vargottama).
"""

from dataclasses import dataclass
from typing import Callable

from app.astrology.derivations import SIGNS, compute_navamsa_sign, sign_index

_EPSILON = 1e-9

_ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}


def _make_varga_fn(divisions: int, start_offset: Callable[[str], int]) -> Callable[[str, float], str]:
    span = 30 / divisions

    def compute(sign: str, degree_in_sign: float) -> str:
        index = int((degree_in_sign + _EPSILON) // span)
        index = min(index, divisions - 1)  # guards a degree of exactly 30 (should not occur, but stay in-range)
        start = (sign_index(sign) + start_offset(sign)) % 12
        return SIGNS[(start + index) % 12]

    return compute


def _saptamsa_offset(sign: str) -> int:
    # Odd signs count from themselves; even signs count from the 7th sign from them.
    return 0 if sign in _ODD_SIGNS else 6


def _dasamsa_offset(sign: str) -> int:
    # Odd signs count from themselves; even signs count from the 9th sign from them.
    return 0 if sign in _ODD_SIGNS else 8


@dataclass
class VargaDefinition:
    key: str
    label: str
    significance: str
    compute_sign: Callable[[str, float], str]


VARGA_REGISTRY: dict[str, VargaDefinition] = {
    "D9": VargaDefinition(
        key="D9",
        label="Navamsa",
        significance="Marriage, the spouse, and each planet's inner/spiritual strength",
        compute_sign=compute_navamsa_sign,
    ),
    "D7": VargaDefinition(
        key="D7",
        label="Saptamsa",
        significance="Children and creative or generative capacity",
        compute_sign=_make_varga_fn(7, _saptamsa_offset),
    ),
    "D10": VargaDefinition(
        key="D10",
        label="Dasamsa",
        significance="Career, profession and public standing",
        compute_sign=_make_varga_fn(10, _dasamsa_offset),
    ),
    "D12": VargaDefinition(
        key="D12",
        label="Dwadasamsa",
        significance="Parents and ancestry",
        compute_sign=_make_varga_fn(12, lambda sign: 0),
    ),
}


def compute_varga_chart(varga_key: str, lagna_sign: str, lagna_degree: float, planets: list[dict]) -> dict:
    varga = VARGA_REGISTRY[varga_key]
    varga_lagna_sign = varga.compute_sign(lagna_sign, lagna_degree)

    varga_planets = []
    for planet in planets:
        varga_sign = varga.compute_sign(planet["sign"], planet["degree"])
        house = ((sign_index(varga_sign) - sign_index(varga_lagna_sign)) % 12) + 1
        varga_planets.append({"name": planet["name"], "sign": varga_sign, "house": house})

    return {
        "key": varga.key,
        "label": varga.label,
        "significance": varga.significance,
        "lagna": varga_lagna_sign,
        "planets": varga_planets,
    }
