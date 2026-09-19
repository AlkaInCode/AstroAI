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
        "topic": "seventh house",
        "content": (
            "The 7th house traditionally governs marriage, partnerships and "
            "one-to-one relationships, including business partnerships."
        ),
        "source": "Placeholder Phase-1 knowledge note",
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
]


def search_astrology_knowledge(query: str, top_k: int = 3) -> list[dict]:
    query_lower = query.lower()
    scored = [
        entry
        for entry in _PLACEHOLDER_KNOWLEDGE
        if entry["topic"].lower() in query_lower or query_lower in entry["topic"].lower()
    ]
    return scored[:top_k] if scored else _PLACEHOLDER_KNOWLEDGE[:top_k]


def search_numerology_knowledge(query: str, top_k: int = 3) -> list[dict]:
    return []
