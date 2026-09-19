# AstroAI Backend

FastAPI backend for Phase 1: signup/login, birth profile intake, chart generation, and the AI chat assistant.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` with real values when you have them. With no keys set, the app runs against:
- `MockAstrologyProvider` (deterministic placeholder chart data)
- `MockGeocodingProvider`
- `EchoLLMClient` (placeholder chat replies)

so the whole flow is testable end-to-end before any external accounts exist.

## Database

Requires PostgreSQL. Create the database, then run migrations:

```bash
alembic upgrade head
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs`.

## Layout

```
app/
  api/          # route handlers (auth, profiles, charts, chat)
  models/       # SQLAlchemy tables
  schemas/      # Pydantic request/response models
  services/     # security (JWT/hashing), geocoding
  astrology/    # AstrologyProvider interface + provider implementations
  ai/           # agent, tools, prompts, rag, llm client
  database/     # engine/session setup
alembic/        # schema migrations
```

## Swapping providers

- Astrology: set `ASTROLOGY_PROVIDER=prokerala` and fill in `PROKERALA_CLIENT_ID`/`SECRET` once evaluated. Add a new file under `app/astrology/providers/` and register it in `app/astrology/factory.py` to try a different provider (e.g. VedAstro).
- LLM: set `LLM_PROVIDER` / `LLM_MODEL` / `LLM_API_KEY`.
