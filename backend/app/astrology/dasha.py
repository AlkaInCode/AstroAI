"""
Vimshottari Mahadasha / Antardasha / Pratyantardasha calculation.

Vimshottari is the standard 120-year cyclic Dasha system used in Vedic
astrology, keyed off the Moon's Nakshatra at birth. Like every other
astrology/ module here, this is a deterministic rule engine operating on
whatever Moon position a calculation provider supplies -- it never guesses
or invents dates.

The full Mahadasha sequence (with nested Antardashas) is computed for one
full run from birth through roughly the traditional 120-year span.
Pratyantardasha is only computed for the currently active Antardasha --
a full 9x9x9 breakdown for an entire lifetime (729 periods) is far more
data than any dashboard or chat answer needs at once. _split_into_sub_periods
is reusable, so drilling into any other period's Pratyantardasha later is a
one-line call, not a rewrite.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from app.astrology.derivations import NAKSHATRA_SPAN

DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

_TOTAL_CYCLE_YEARS = 120
_DAYS_PER_YEAR = 365.25  # standard convention for converting Dasha years to calendar dates


@dataclass
class DashaPeriod:
    planet: str
    start: date
    end: date

    def to_dict(self) -> dict:
        return {"planet": self.planet, "start": self.start.isoformat(), "end": self.end.isoformat()}


def nakshatra_lord(nakshatra_index: int) -> str:
    return DASHA_ORDER[nakshatra_index % 9]


def _add_years(start: date, years: float) -> date:
    return start + timedelta(days=years * _DAYS_PER_YEAR)


def _split_into_sub_periods(planet: str, start: date, end: date) -> list[DashaPeriod]:
    """Splits [start, end) into 9 sub-periods, one per planet in DASHA_ORDER
    starting from `planet` itself, each sized proportional to that planet's
    share of the 120-year cycle. This same formula applies whether splitting
    a Mahadasha into Antardashas or an Antardasha into Pratyantardashas."""
    total_days = (end - start).days
    start_index = DASHA_ORDER.index(planet)

    periods = []
    cursor = start
    for i in range(9):
        sub_planet = DASHA_ORDER[(start_index + i) % 9]
        share = DASHA_YEARS[sub_planet] / _TOTAL_CYCLE_YEARS
        sub_end = cursor + timedelta(days=total_days * share)
        periods.append(DashaPeriod(sub_planet, cursor, sub_end))
        cursor = sub_end

    # Floating-point day fractions can drift the last boundary by a hair; snap it to `end` exactly.
    if periods:
        periods[-1] = DashaPeriod(periods[-1].planet, periods[-1].start, end)
    return periods


def compute_mahadasha_sequence(dob: date, moon_longitude: float) -> list[DashaPeriod]:
    """One full run through all 9 planets starting from whichever planet
    rules the Moon's Nakshatra at birth. The first Mahadasha is only a
    partial (balance) period -- however much of it hadn't yet elapsed,
    proportionally, when the Moon was at its exact birth position within
    that Nakshatra."""
    moon_longitude = moon_longitude % 360
    nakshatra_index = int(moon_longitude // NAKSHATRA_SPAN)
    position_in_nakshatra = moon_longitude - nakshatra_index * NAKSHATRA_SPAN
    elapsed_fraction = position_in_nakshatra / NAKSHATRA_SPAN

    first_lord = nakshatra_lord(nakshatra_index)
    start_index = DASHA_ORDER.index(first_lord)

    periods = []
    cursor = dob
    for i in range(9):
        planet = DASHA_ORDER[(start_index + i) % 9]
        full_years = DASHA_YEARS[planet]
        duration_years = full_years * (1 - elapsed_fraction) if i == 0 else full_years
        end = _add_years(cursor, duration_years)
        periods.append(DashaPeriod(planet, cursor, end))
        cursor = end
    return periods


def _find_current(periods: list[DashaPeriod], as_of: date) -> DashaPeriod | None:
    return next((p for p in periods if p.start <= as_of < p.end), None)


def compute_dasha(dob: date, moon_longitude: float, as_of: date | None = None) -> dict:
    as_of = as_of or date.today()
    mahadashas = compute_mahadasha_sequence(dob, moon_longitude)

    mahadasha_sequence = []
    current_mahadasha = None
    current_antardasha = None
    current_pratyantardasha = None
    current_pratyantardasha_sequence: list[dict] = []

    for md in mahadashas:
        antardashas = _split_into_sub_periods(md.planet, md.start, md.end)
        is_current_md = md.start <= as_of < md.end

        for ad in antardashas:
            if is_current_md and ad.start <= as_of < ad.end:
                current_antardasha = ad.to_dict()
                pratyantardashas = _split_into_sub_periods(ad.planet, ad.start, ad.end)
                current_pratyantardasha_sequence = [pd.to_dict() for pd in pratyantardashas]
                current_pad = _find_current(pratyantardashas, as_of)
                if current_pad:
                    current_pratyantardasha = current_pad.to_dict()

        mahadasha_sequence.append({**md.to_dict(), "antardashas": [ad.to_dict() for ad in antardashas]})
        if is_current_md:
            current_mahadasha = md.to_dict()

    return {
        "mahadasha_sequence": mahadasha_sequence,
        "current_mahadasha": current_mahadasha,
        "current_antardasha": current_antardasha,
        "current_pratyantardasha": current_pratyantardasha,
        "current_pratyantardasha_sequence": current_pratyantardasha_sequence,
    }
