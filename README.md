# AstroAI

AI-first Vedic Astrology & Numerology platform.

A customer signs up, enters their birth details once, and receives an accurately calculated Kundli (birth chart). On top of that chart sits an AI assistant that answers natural-language questions about the customer's own chart — grounded in real calculated data and a curated astrology knowledge base, never guessed.

## Project Status

**Phase 1** is built and verified end-to-end: signup, login, birth profile intake, chart generation (mock provider), the Kundli dashboard, and the AI chat all work against a real local PostgreSQL database.

**Phase 2** (planetary detail) is also built and verified: every planet placement now carries Nakshatra, Pada, combustion, exaltation/debilitation, Vargottama, and Parashari aspects — computed by a shared, provider-agnostic rule engine (`backend/app/astrology/derivations.py`) so any calculation provider gets these attributes consistently.

**Phase 3** (better personal analysis) is also built and verified: the Personality/Career/Love/Money/General life-area cards now reason over house lords and each significator's actual dignity/combustion state, with a short RAG-grounded knowledge note per card (`backend/app/ai/life_areas.py`). Real API keys (astrology + LLM) are intentionally not wired in yet — see the docs below for the full plan.

## Where to Start

- [`planning/PROJECT_PLAN.md`](planning/PROJECT_PLAN.md) — plain-language summary of what we're building, why, and what's decided so far.
- [`docs/PRD.md`](docs/PRD.md) — full product requirements document (architecture, data model, tech stack, phased roadmap).
- [`backend/README.md`](backend/README.md) — backend setup.
- [`frontend/README.md`](frontend/README.md) — frontend setup.

## Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Python + FastAPI + SQLAlchemy + Pydantic
- **Database:** PostgreSQL (native Windows install, no Docker)
- **Astrology calculation:** external API, abstracted behind an internal interface — mock provider for local dev, Prokerala integration ready for real credentials
- **AI:** LLM + tool-calling + RAG, backend-only

## Running Locally

1. PostgreSQL running as a Windows service, with the `astroai` database/user created (see `backend/README.md`).
2. Backend: `cd backend`, create a venv, `pip install -r requirements.txt`, copy `.env.example` to `.env`, `alembic upgrade head`, then `uvicorn app.main:app --reload`.
3. Frontend: `cd frontend`, `npm install`, `npm run dev`.

## Repository Layout

```
backend/    # FastAPI backend
frontend/   # React frontend
docs/       # Detailed PRD
planning/   # Running plain-language project plan
```
