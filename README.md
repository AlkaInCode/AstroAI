# AstroAI

AI-first Vedic Astrology & Numerology platform.

A customer signs up, enters their birth details once, and receives an accurately calculated Kundli (birth chart). On top of that chart sits an AI assistant that answers natural-language questions about the customer's own chart — grounded in real calculated data and a curated astrology knowledge base, never guessed.

## Project Status

**Phase 1** is built and verified end-to-end: signup, login, birth profile intake, chart generation (mock provider), the Kundli dashboard, and the AI chat all work against a real local PostgreSQL database.

**Phase 2** (planetary detail) is also built and verified: every planet placement now carries Nakshatra, Pada, combustion, exaltation/debilitation, Vargottama, and Parashari aspects — computed by a shared, provider-agnostic rule engine (`backend/app/astrology/derivations.py`) so any calculation provider gets these attributes consistently.

**Phase 3** (better personal analysis) is also built and verified: the Personality/Career/Love/Money/General life-area cards now reason over house lords and each significator's actual dignity/combustion state, with a short RAG-grounded knowledge note per card (`backend/app/ai/life_areas.py`).

**Phase 4** (Vimshottari Dasha) is also built and verified: full Mahadasha/Antardasha timeline from birth, current Mahadasha/Antardasha/Pratyantardasha resolution as of today, a dashboard timeline UI, and the AI chat is now grounded with the customer's current Dasha (`backend/app/astrology/dasha.py`).

**Phase 5** (Yogas/Rajyogas) is also built and verified: a deterministic Yoga engine (`backend/app/astrology/yogas.py`) detects the five Pancha Mahapurusha Yogas, Gajakesari, Budhaditya, Chandra-Mangal, Raja, and Dhana Yogas from real chart facts — never guessed by the LLM — shown as dashboard cards and grounding the AI chat.

**Phase 6** (Divisional Charts) is also built and verified: reusable Varga infrastructure (`backend/app/astrology/vargas.py`) computes D9/Navamsa, D7/Saptamsa, D10/Dasamsa and D12/Dwadasamsa from a single generic formula — adding another divisional chart later is one registry entry, not a new calculator. Required adding the Ascendant's precise degree to the chart model (previously only its sign was stored), which a real astrology API will need to supply too.

**Phase 7** (Transits) is also built and verified: current planetary transit positions (`backend/app/astrology/transits.py`) combined with each customer's natal Lagna and Moon, with deterministic Sade Sati and Jupiter Return detection, a date-pickable transit view on the dashboard, and transits grounding the AI chat.

**Numerology** (parallel track) is also built and verified: Life Path, Expression, Soul Urge, Personality and Chaldean Destiny numbers computed deterministically from name and birth date (`backend/app/numerology/calculations.py`, correctly preserving Master Numbers 11/22/33), persisted per profile, shown as dashboard cards, and grounding the AI chat.

**My Clients** (parallel track) is also built and verified: an account can hold multiple birth profiles (e.g. family members), with a searchable list, inline name editing, and delete (`frontend/src/pages/Clients.jsx` + profile PATCH/DELETE endpoints) — `/dashboard` now goes straight to the one Kundli for single-profile accounts, or to the clients list once there's more than one. Real API keys (astrology + LLM) are intentionally not wired in yet — see the docs below for the full plan.

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
