# AstroAI Backend

FastAPI backend for Phase 1: signup/login, birth profile intake, chart generation, and the AI chat assistant.

Prefer running this via `docker compose up --build` from the repo root (see the top-level README) unless you specifically need to run it natively.

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

- Astrology: `ASTROLOGY_PROVIDER=mock` (default), `astroengine`, or `prokerala`.
  - `astroengine` calls a self-hosted [AstroEngine](https://github.com/thebrownhuman/AstroEngine) instance (no API key) -- set `ASTROENGINE_BASE_URL` to where it's running (LAN IP, or `host.docker.internal:8000` when the backend itself runs in Docker and AstroEngine runs on the host machine).
  - `prokerala` needs `PROKERALA_CLIENT_ID`/`SECRET` once evaluated.
  - Add a new file under `app/astrology/providers/` and register it in `app/astrology/factory.py` to try a different provider.
- LLM: set `LLM_PROVIDER` / `LLM_MODEL` / `LLM_API_KEY`.
