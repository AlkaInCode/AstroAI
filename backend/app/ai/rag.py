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
