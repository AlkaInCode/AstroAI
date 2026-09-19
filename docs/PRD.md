# Product Requirements Document — AI Vedic Astrology & Numerology Platform

**Owner:** Shivansh
**Status:** Draft v1.0 — Phase 1 (MVP) scope
**Last updated:** 2026-09-19

---

## 1. Product Definition

An AI-powered Vedic Astrology (and later Numerology) platform where a customer self-signs up, enters their birth details once, receives a permanently-stored, accurately-calculated Kundli (birth chart), sees a plain-language breakdown of their personality/career/love/money, and can chat with an AI assistant that answers personalized questions using their real chart data plus trusted astrology knowledge — never guessed or hallucinated facts.

**Core loop:** Sign up → Enter Birth Details → Calculate Kundli → Save → View Chart + Life-Area Descriptions → Ask AI Anything About It.

---

## 2. Goals & Non-Goals (Phase 1)

### Goals
- Public self-signup — anyone can create an account and generate their own Kundli.
- Every chart calculation is backed by a real deterministic astrology engine (API), never invented by the LLM.
- Client + chart + conversation data is permanently stored (PostgreSQL) and reopenable anytime.
- Customer gets a readable Kundli dashboard (Lagna, Rashi, planets, houses, degrees) plus a short plain-language life-area writeup (personality, career, love, money, general themes).
- An AI chat assistant, scoped to the customer's own chart, answers natural-language questions grounded in calculated chart data + curated astrology knowledge (RAG).
- Cute, soft, light-blue, modern, feminine UI — approachable for non-astrologers.

### Non-Goals (explicitly deferred to later phases)
- Dasha, Yogas/Rajyogas, divisional charts (D9 etc.), transits, nakshatra/pada detail, retrograde/combust/exalted flags — Phase 2+.
- Numerology — parallel track, later phase.
- Astrologer/Admin dashboard for managing other people's clients — later phase (Phase 1 is self-service only).
- Fine-tuning any model.
- Payments/subscriptions (not in scope for this PRD; flag separately if needed).
- Native mobile apps (web-responsive only for now).

---

## 3. Users

- **Primary: Self-signup customer.** Wants to know their own chart and get simple, trustworthy answers about themselves. Not an astrology expert.
- **(Deferred) Astrologer/Admin.** Will eventually manage multiple clients — out of scope for Phase 1 build, but data model must not block adding this later (see §11).

---

## 4. End-to-End User Flow (Phase 1)

1. Visitor lands on the site → sees a soft, inviting landing page explaining the product.
2. Visitor signs up (email + password) and verifies/logs in.
3. Logged-in user is prompted to create their birth profile: Full name, Gender, DOB, exact birth time, birth place (city search → resolves lat/long/timezone), state, country.
4. Frontend validates inputs (required fields, valid date/time, place resolved to coordinates).
5. Backend sends birth details to the astrology calculation API.
6. Calculation returns Lagna/Ascendant, Rashi, planetary positions (sign, house, degree), Ayanamsa/system used.
7. Backend stores birth profile + chart result in PostgreSQL, linked to the user's account.
8. User is redirected to their Kundli Dashboard: chart visualization + planet table + basic life-area write-up (personality/career/love/money/general).
9. Below the dashboard, an AI Chat box is available, pre-scoped to this user's chart (no need to repeat birth info).
10. User asks questions ("What's my Moon sign?" / "Tell me about my career"); AI calls chart-data tools, retrieves relevant RAG knowledge, and responds in plain language, clearly separating calculated fact from traditional interpretation.
11. User can log out and log back in anytime; their profile, chart, and full chat history persist and reload instantly (no re-entry).
12. A logged-in user can hold exactly one primary birth profile in Phase 1 (multi-profile per account — e.g. adding family members — is a fast-follow, not required for MVP).

---

## 5. Functional Requirements

### 5.1 Authentication & Accounts
- Email + password signup/login (hashed passwords, standard session/JWT auth).
- Logged-out users can view the landing page only; chart creation and AI chat require login.
- Password reset flow (basic, can use email link).

### 5.2 Birth Details Intake
- Fields: Full name, gender (male/female, extensible enum — not hardcoded to 2 values at the DB level), DOB (date picker), exact birth time (time picker, required in Phase 1 — UI should note why accuracy matters), birth place (typeahead city search).
- City search resolves to latitude, longitude, and timezone via a geocoding service (e.g. Google Places/OpenCage/Geonames — pick one abstracted provider) and stores all three.
- Client-side + server-side validation before submission.

### 5.3 Chart Calculation
- Backend calls a single primary external astrology API (astrology calculation is never done by the LLM and never hardcoded).
- Recommended primary provider: **Prokerala Astrology API** (Swiss-Ephemeris-based, well documented, supports Lagna/Rashi/planetary positions/houses; has a workable free/paid tier). Keep the integration behind an internal interface (`AstrologyProvider`) so the provider can be swapped or a secondary validation provider added later without touching the rest of the app.
- Explicitly record and store, per chart: Ayanamsa used, house system used, Rahu/Ketu method, calculation provider name/version — so results are auditable and reproducible.
- Returned data persisted: Lagna/Ascendant, Rashi, each planet's sign/house/degree, raw provider response (for future reprocessing without re-calling the API).

### 5.4 Kundli Dashboard
- Header: name, DOB, birth time, birth place.
- North Indian style Lagna/Rashi chart visualization.
- Planet table: planet, sign, house, degree.
- Life-area description cards, generated from the actual chart data (not generic horoscope filler): Personality, Career, Love/Relationships, Money/Finance, General life themes. Phase 1 wording can be templated from chart facts (e.g., rule-based sentence construction keyed off sign/house placements) or produced by the LLM using the chart-fact tool + RAG — either way, must cite the underlying chart facts, not invent them.

### 5.5 AI Chat Assistant
- Chat UI directly below/attached to the Kundli dashboard.
- Every message is scoped server-side to the logged-in user's current chart (chart ID injected into context — user never has to state their birth info to the AI).
- Backend AI agent architecture (see §6): LLM + tool-calling + RAG, never the LLM inventing chart facts.
- Full conversation history stored per user and reloaded on return visits.
- Answer style: plain language by default; clearly labels which parts are "calculated fact" vs. "traditional interpretation"; never states astrological interpretation as scientific fact.

### 5.6 Data Persistence
- PostgreSQL is the system of record for: users/auth, birth profiles, charts (incl. raw provider payload), conversations/messages.
- Nothing the user has entered or been shown is ever re-derived from scratch on a return visit — always reloaded from DB; re-calculation only happens if the user explicitly edits birth details.

---

## 6. AI Architecture (Phase 1 scope)

Layered system — no single "do everything" model:

| Layer | Responsibility | Phase 1 detail |
|---|---|---|
| Astrology Calculation Engine/API | Ground-truth chart facts | Prokerala API (abstracted) |
| PostgreSQL | Permanent storage of user, chart, chat | SQLAlchemy models |
| RAG Knowledge Base | Trusted astrology reference retrieval | pgvector + curated public-domain/licensed sources on planets/houses/signs (minimum viable set for Phase 1: general planet-in-sign, planet-in-house, and life-area meanings) |
| LLM | NL understanding, tool selection, reasoning, explanation | Backend-only call, provider/model configurable via env vars |
| AI Tools | Controlled functions the LLM may call | Phase 1 subset: `get_profile`, `get_birth_details`, `get_chart`, `get_planet_details`, `get_house_details`, `search_astrology_knowledge`, `get_chat_history` |

Rule enforced in the system prompt and validated in code: the LLM must call a tool for any chart-specific fact and must call RAG search for any traditional-knowledge claim; it must not answer factual chart questions from its own "knowledge."

Example flow — "What does Saturn mean for my career?":
1. Identify current user's chart ID from session.
2. `get_planet_details(chart_id, "Saturn")` → sign/house/degree/retrograde.
3. `search_astrology_knowledge("Saturn career 10th house")` → relevant curated passages.
4. LLM composes an answer from both, in plain language.

---

## 7. Non-Functional Requirements

- **Security/Privacy:** hashed passwords, HTTPS, LLM/astrology API keys backend-only (never in frontend bundle), env-var secrets, DB access controls, minimal sensitive logging, basic backup strategy.
- **Reliability of calculation:** deterministic engine only; no cached/mock planetary data in production; document the exact Ayanamsa/house-system/Rahu-Ketu convention used so results are consistent and explainable.
- **Performance:** Kundli dashboard should load from DB (not recompute) in under ~1s for a returning user; initial calculation + AI first response can be a few seconds (show loading state).
- **Extensibility:** DB schema and service layer must not block adding later: multiple profiles per user, admin/astrologer role, numerology, dasha/yoga/transit fields, divisional charts. Prefer additive columns/tables over redesign.

---

## 8. UI/UX Direction

- Palette: primary very light blue; supporting white, soft pink, lavender, light blue-gray, dark gray text.
- Rounded cards, soft shadows, generous spacing, friendly iconography, clean typography, fully responsive (mobile-first, since many users will sign up from phones).
- Tone: cute, calm, modern, beginner-friendly — explicitly avoid the cluttered/dark "old astrology website" look.
- Key screens for Phase 1: Landing page, Sign up/Login, Birth Details form (multi-step: identity → DOB/time → place), Kundli Dashboard (chart + planet table + life-area cards), AI Chat (integrated panel, not a separate page).

---

## 9. Tech Stack

- **Frontend:** React + Vite + Tailwind CSS + React Router.
- **Backend:** Python + FastAPI + Pydantic + SQLAlchemy.
- **Database:** PostgreSQL + pgvector (for RAG embeddings).
- **Astrology API:** Prokerala Astrology API (primary, abstracted behind an internal provider interface).
- **Geocoding:** one abstracted provider (e.g. OpenCage or Google Places) for place → lat/long/timezone.
- **LLM:** configurable via `LLM_PROVIDER` / `LLM_MODEL` env vars; called only from backend.

### Suggested backend structure
```
backend/
  app/
    api/            # route handlers
    models/         # SQLAlchemy DB models
    schemas/         # Pydantic request/response schemas
    services/        # business logic
    repositories/    # DB access
    database/
    astrology/
      provider.py     # AstrologyProvider interface + Prokerala implementation
      chart.py
      planets.py
      houses.py
    ai/
      agent.py
      tools.py
      prompts.py
      rag.py
      llm.py
```

---

## 10. Data Model (Phase 1)

**users** — id, email, password_hash, created_at

**birth_profiles** — id, user_id (FK), full_name, gender, dob, birth_time, birth_place, city, state, country, latitude, longitude, timezone, created_at, updated_at

**charts** — id, birth_profile_id (FK), lagna, rashi, ayanamsa, house_system, calculation_provider, planetary_data (JSON), raw_provider_response (JSON), created_at

**conversations** — id, birth_profile_id (FK), session_id, role (user/assistant), message, created_at

**knowledge_chunks** (RAG) — id, title, author, tradition, system, chapter, topic, source, rights_status, content, embedding (vector)

---

## 11. Forward Compatibility Notes (not built now, but must not be blocked)

- `gender` stored as a flexible enum, not a boolean.
- `birth_profiles.user_id` relationship designed so a user could later own >1 profile (family members) without schema rewrite.
- `charts` table designed to hold future fields (dasha, yogas, transits) as additive JSON or new related tables, not by altering existing columns.
- A `role` field on `users` (default `"customer"`) reserved for the future `astrologer/admin` role, even though Phase 1 has no admin UI.
- Numerology will reuse the same `birth_profile_id` foreign-key pattern and its own `numerology_results` table later.

---

## 12. Success Criteria (Phase 1 "done")

> A new visitor can sign up, enter their birth details once, immediately see an accurately calculated Kundli with a plain-language personality/career/love/money summary, ask the AI natural questions about that exact chart and get answers grounded in real chart data and cited astrology knowledge, log out, log back in later, and find everything — chart and full chat history — exactly as they left it.

---

## 13. Open Items / Decisions Needed Before Build

- Confirm Prokerala API pricing tier fits expected signup volume (or fall back to self-hosted Swiss Ephemeris if cost is a blocker).
- Also evaluate **VedAstro** (advertises Dasha/Yoga/transit calculations, Chaldean numerology, and a classical-text retrieval API) and **Rajvidya** (advertises combined astrology + numerology) as possible single-provider alternatives to Prokerala — if either proves accurate and stable, it could reduce the number of external integrations needed for Phase 4+ (Dasha/Yoga) and the numerology track. Treat all provider names in this document as technical references to evaluate, not a final ranking — pricing/endpoints/terms shift over time and must be re-checked at build time.
- Choose one geocoding provider.
- Decide initial LLM provider/model (any modern Claude or GPT model works given the tool-calling architecture).
- Assemble the minimum Phase-1 RAG source set (a handful of public-domain planet/house/sign meaning texts is enough to start — full classical text ingestion is Phase 2+).

---

## 14. Roadmap (unchanged from source vision, for reference)

Phase 1 (this PRD) → Phase 2: Nakshatra/Pada/Retrograde/Combust/Exalted/Debilitated/Vargottama/Aspects → Phase 3: deeper life-area analysis → Phase 4: Dasha → Phase 5: Yogas/Rajyogas → Phase 6: Divisional charts → Phase 7: Transits & calendar → Phase 8: full agentic "what's happening in my chart right now" assistant. Numerology and the Astrologer/Admin dashboard run as parallel tracks once Phase 1 is stable.
