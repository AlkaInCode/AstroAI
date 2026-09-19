# AstroAI

AI-first Vedic Astrology & Numerology platform.

A customer signs up, enters their birth details once, and receives an accurately calculated Kundli (birth chart). On top of that chart sits an AI assistant that answers natural-language questions about the customer's own chart — grounded in real calculated data and a curated astrology knowledge base, never guessed.

## Project Status

Planning phase. No application code yet — see the docs below for the full plan before any implementation begins.

## Where to Start

- [`planning/PROJECT_PLAN.md`](planning/PROJECT_PLAN.md) — plain-language summary of what we're building, why, and what's decided so far.
- [`docs/PRD.md`](docs/PRD.md) — full product requirements document (architecture, data model, tech stack, phased roadmap).

## Planned Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Python + FastAPI + SQLAlchemy + Pydantic
- **Database:** PostgreSQL + pgvector
- **Astrology calculation:** external API (primary: Prokerala, abstracted behind an internal interface)
- **AI:** LLM + tool-calling + RAG, backend-only

## Repository Layout

```
backend/    # FastAPI backend (to be built)
frontend/   # React frontend (to be built)
docs/       # Detailed PRD
planning/   # Running plain-language project plan
```
