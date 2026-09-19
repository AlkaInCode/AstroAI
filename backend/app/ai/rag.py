"""
RAG knowledge retrieval over curated astrology/numerology sources.

Phase 1 ships a minimal in-memory keyword lookup so the agent has *some*
grounded knowledge to cite without requiring pgvector + an embeddings
pipeline to be wired up first. Swap search_astrology_knowledge's body for a
real pgvector similarity query once the knowledge_chunks table (PRD S10) is
populated -- callers do not need to change.
"""

_PLACEHOLDER_KNOWLEDGE = [
    {
        "topic": "Saturn",
        "content": (
            "In classical Vedic astrology, Saturn (Shani) represents discipline, "
            "delay, responsibility and long-term structure. Its placement by house "
            "and sign shapes where a person experiences the most restriction and, "
            "over time, the most durable mastery."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Jupiter",
        "content": (
            "Jupiter (Guru) represents expansion, wisdom, wealth and good fortune. "
            "Its house placement traditionally indicates the life area where growth "
            "and opportunity come most naturally."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Moon",
        "content": (
            "The Moon (Chandra) represents the mind, emotions and instinctive "
            "reactions. Its sign is the Rashi, often considered as important as the "
            "Lagna for understanding personality and emotional temperament."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Sun",
        "content": (
            "The Sun (Surya) represents identity, willpower, authority and vitality. "
            "As a house lord, it points to where a person seeks recognition and asserts themselves."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Mars",
        "content": (
            "Mars (Mangal) represents courage, drive, action and assertiveness. "
            "As a house lord, it shows where a person acts decisively and where conflict may arise."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Mercury",
        "content": (
            "Mercury (Budha) represents intellect, communication and analytical thinking. "
            "As a house lord, it points to where a person reasons things through before acting."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Venus",
        "content": (
            "Venus (Shukra) represents love, beauty, harmony and material comfort. "
            "As a house lord, it shows where a person seeks pleasure, connection and refinement."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "seventh house",
        "content": (
            "The 7th house traditionally governs marriage, partnerships and "
            "one-to-one relationships, including business partnerships."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Lagna",
        "content": (
            "The Lagna (Ascendant) is the zodiac sign rising on the eastern horizon at "
            "the moment of birth. It sets the chart's overall frame of reference -- "
            "house 1 -- and its ruling planet, the Lagna lord, is often read as the "
            "single most important indicator of a person's general life direction."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "tenth house",
        "content": (
            "The 10th house traditionally governs career, public standing, "
            "authority and one's actions in the world."
        ),
        "source": "Placeholder Phase-1 knowledge note",
    },
    {
        "topic": "Nakshatra",
        "content": (
            "Each planet's Nakshatra (lunar mansion) is one of 27 divisions of the "
            "zodiac, each further split into four Padas (quarters). The Nakshatra "
            "adds a finer layer of meaning beyond the sign, especially for the Moon."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "combust",
        "content": (
            "A planet is considered combust when it sits too close to the Sun. "
            "Classically this is thought to weaken the planet's ability to express "
            "its own significations clearly, as its light is 'overpowered' by the Sun's."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "exalted",
        "content": (
            "A planet is exalted in a specific sign where its qualities are "
            "traditionally considered strongest and most naturally expressed."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "debilitated",
        "content": (
            "A planet is debilitated in the sign directly opposite its exaltation "
            "sign, where its qualities are traditionally considered weakest or most "
            "challenged -- though this can also point to areas needing conscious effort."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "Vargottama",
        "content": (
            "A planet is Vargottama when it occupies the same sign in both the "
            "birth chart (Rashi/D1) and the Navamsa chart (D9). This is traditionally "
            "considered a strengthening placement, reinforcing that planet's results."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "aspects",
        "content": (
            "In Parashari Vedic astrology, every planet casts a full aspect on the "
            "house 7 positions from itself. Mars, Jupiter and Saturn have additional "
            "special aspects: Mars aspects the 4th and 8th, Jupiter the 5th and 9th, "
            "and Saturn the 3rd and 10th houses from its own position."
        ),
        "source": "Placeholder Phase-2 knowledge note",
    },
    {
        "topic": "Mahadasha",
        "content": (
            "Vimshottari Mahadasha is a 120-year cyclic system of planetary periods, "
            "keyed off the Moon's Nakshatra at birth. Each of the 9 grahas rules a "
            "Mahadasha of a fixed length, and the planet running at any given time is "
            "considered a major influence on the themes active in a person's life then."
        ),
        "source": "Placeholder Phase-4 knowledge note",
    },
    {
        "topic": "Antardasha",
        "content": (
            "Within each Mahadasha, an Antardasha (sub-period) of every planet occurs "
            "in turn, starting with the Mahadasha's own planet. The Antardasha planet "
            "adds its own flavor on top of the ruling Mahadasha, refining the timing "
            "of when a particular theme is most active."
        ),
        "source": "Placeholder Phase-4 knowledge note",
    },
    {
        "topic": "Ruchaka Yoga",
        "content": (
            "Ruchaka Yoga forms when Mars is in its own sign or exalted while placed in "
            "a kendra (angular house). It is one of the five Pancha Mahapurusha Yogas, "
            "traditionally associated with courage, physical strength and leadership."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Bhadra Yoga",
        "content": (
            "Bhadra Yoga forms when Mercury is in its own sign or exalted while placed in "
            "a kendra (angular house). It is one of the five Pancha Mahapurusha Yogas, "
            "traditionally associated with sharp intellect and communication skill."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Hamsa Yoga",
        "content": (
            "Hamsa Yoga forms when Jupiter is in its own sign or exalted while placed in "
            "a kendra (angular house). It is one of the five Pancha Mahapurusha Yogas, "
            "traditionally associated with wisdom, ethics and respect from others."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Malavya Yoga",
        "content": (
            "Malavya Yoga forms when Venus is in its own sign or exalted while placed in "
            "a kendra (angular house). It is one of the five Pancha Mahapurusha Yogas, "
            "traditionally associated with charm, comfort and artistic sensibility."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Sasa Yoga",
        "content": (
            "Sasa Yoga forms when Saturn is in its own sign or exalted while placed in "
            "a kendra (angular house). It is one of the five Pancha Mahapurusha Yogas, "
            "traditionally associated with discipline, authority and enduring achievement."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Gajakesari Yoga",
        "content": (
            "Gajakesari Yoga forms when Jupiter is positioned in a kendra (1st, 4th, 7th "
            "or 10th house) counted from the Moon. It is traditionally considered to bring "
            "intelligence, good reputation and general good fortune."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Budhaditya Yoga",
        "content": (
            "Budhaditya Yoga forms when the Sun and Mercury are conjunct in the same "
            "house. It is traditionally associated with sharp intellect, analytical "
            "ability and success through communication or scholarship."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Chandra-Mangal Yoga",
        "content": (
            "Chandra-Mangal Yoga forms when the Moon and Mars are conjunct in the same "
            "house. It is traditionally read as a wealth-producing combination, though "
            "one that can also bring emotional intensity."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Raja Yoga",
        "content": (
            "A Raja Yoga classically forms when the lord of a kendra (angular) house and "
            "the lord of a trikona (trinal) house join together -- by conjunction, mutual "
            "aspect, or sign exchange. It is considered one of the most auspicious "
            "combinations, traditionally linked to status, authority and success."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Dhana Yoga",
        "content": (
            "A Dhana Yoga (wealth combination) classically forms when the lords of the "
            "wealth houses -- most commonly the 2nd (accumulated wealth) and 11th "
            "(gains) -- join together, indicating a capacity for financial prosperity."
        ),
        "source": "Placeholder Phase-5 knowledge note",
    },
    {
        "topic": "Sade Sati",
        "content": (
            "Sade Sati is the roughly 7.5-year period when transiting Saturn moves "
            "through the 12th, 1st and 2nd houses counted from a person's natal Moon "
            "sign (about 2.5 years in each). It is traditionally considered a period of "
            "significant restructuring, discipline and long-term life lessons."
        ),
        "source": "Placeholder Phase-7 knowledge note",
    },
    {
        "topic": "Jupiter Return",
        "content": (
            "A Jupiter Return occurs when transiting Jupiter comes back to the same "
            "sign it occupied at birth, roughly every 12 years as Jupiter completes one "
            "orbit. It is traditionally considered a period of renewed growth, "
            "opportunity and expansion in the themes that natal Jupiter represents."
        ),
        "source": "Placeholder Phase-7 knowledge note",
    },
    {
        "topic": "Rahu",
        "content": (
            "Rahu is a shadow point (the Moon's ascending lunar node) representing "
            "obsession, ambition and worldly desire. As a house lord or through "
            "transit, it points to where a person feels an intense, sometimes "
            "unconventional pull to achieve and expand."
        ),
        "source": "Placeholder Phase-7 knowledge note",
    },
    {
        "topic": "Ketu",
        "content": (
            "Ketu is a shadow point (the Moon's descending lunar node) representing "
            "detachment, introspection and past-life karma. Through transit, it "
            "points to where a person may feel drawn to release, withdraw from, or "
            "spiritually transcend material concerns."
        ),
        "source": "Placeholder Phase-7 knowledge note",
    },
    {
        "topic": "transit",
        "content": (
            "A transit is the current real-time position of a planet as it moves "
            "through the zodiac, read against the houses of a person's unchanging "
            "natal chart. Transits are considered to activate or trigger the themes of "
            "whichever natal house and planets they currently move through."
        ),
        "source": "Placeholder Phase-7 knowledge note",
    },
]


def search_astrology_knowledge(query: str, top_k: int = 3, allow_fallback: bool = True) -> list[dict]:
    query_lower = query.lower()
    scored = [
        entry
        for entry in _PLACEHOLDER_KNOWLEDGE
        if entry["topic"].lower() in query_lower or query_lower in entry["topic"].lower()
    ]
    if scored:
        return scored[:top_k]
    return _PLACEHOLDER_KNOWLEDGE[:top_k] if allow_fallback else []


def search_numerology_knowledge(query: str, top_k: int = 3) -> list[dict]:
    return []
