"""
Deterministic numerology calculations.

Same architecture principle as the astrology side: these are pure rule
engines over a birth date and a full name, never guessed or invented.
The LLM's job (in app.ai) is only ever to explain a number that was
actually computed here.

Two independent letter-to-number systems are supported -- Pythagorean
(the modern, sequential A-Z mapping) and Chaldean (the older mapping with
no letter valued 9). The Life Path number is date-based and identical
under either system.
"""

from datetime import date

_MASTER_NUMBERS = {11, 22, 33}
_VOWELS = set("AEIOU")

# Pythagorean: A-Z map sequentially onto 1-9, repeating (A=1..I=9, J=1..R=9, S=1..Z=8).
PYTHAGOREAN_MAP = {letter: (i % 9) + 1 for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}

# Chaldean: the older, non-sequential mapping; no letter is ever valued 9.
CHALDEAN_MAP = {
    "A": 1, "I": 1, "J": 1, "Q": 1, "Y": 1,
    "B": 2, "K": 2, "R": 2,
    "C": 3, "G": 3, "L": 3, "S": 3,
    "D": 4, "M": 4, "T": 4,
    "E": 5, "H": 5, "N": 5, "X": 5,
    "U": 6, "V": 6, "W": 6,
    "O": 7, "Z": 7,
    "F": 8, "P": 8,
}


def reduce_number(n: int) -> int:
    """Repeatedly sums digits until a single digit remains, EXCEPT a Master
    Number (11, 22, 33) reached at any step is preserved, not reduced further."""
    while n > 9 and n not in _MASTER_NUMBERS:
        n = sum(int(digit) for digit in str(n))
    return n


def life_path_number(dob: date) -> int:
    """Standard method: reduce month, day and year separately (each may
    resolve to a Master Number), sum those three, then reduce the total."""
    month_reduced = reduce_number(dob.month)
    day_reduced = reduce_number(dob.day)
    year_reduced = reduce_number(dob.year)
    return reduce_number(month_reduced + day_reduced + year_reduced)


def _letter_values(full_name: str, mapping: dict[str, int], predicate) -> list[int]:
    return [mapping[ch] for ch in full_name.upper() if ch.isalpha() and predicate(ch)]


def name_number(full_name: str, mapping: dict[str, int] = PYTHAGOREAN_MAP, only: str = "all") -> int:
    """only: 'all' (Expression/Destiny), 'vowels' (Soul Urge), or 'consonants' (Personality)."""
    if only == "vowels":
        predicate = lambda ch: ch in _VOWELS
    elif only == "consonants":
        predicate = lambda ch: ch not in _VOWELS
    else:
        predicate = lambda ch: True

    values = _letter_values(full_name, mapping, predicate)
    return reduce_number(sum(values)) if values else 0


def compute_numerology(full_name: str, dob: date) -> dict:
    return {
        "full_name_used": full_name,
        "life_path_number": life_path_number(dob),
        "expression_number": name_number(full_name, PYTHAGOREAN_MAP, "all"),
        "soul_urge_number": name_number(full_name, PYTHAGOREAN_MAP, "vowels"),
        "personality_number": name_number(full_name, PYTHAGOREAN_MAP, "consonants"),
        "chaldean_destiny_number": name_number(full_name, CHALDEAN_MAP, "all"),
    }
