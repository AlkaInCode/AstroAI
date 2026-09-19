# AstroAi — Project Plan (Everything Decided So Far)

**Last updated:** 2026-09-19
**Purpose of this file:** a single place to look back at — what we're building, why, what we already decided, and what the final result should look like. Full detailed spec lives in [`../docs/PRD.md`](../docs/PRD.md); this file is the plain-language summary/log of our planning conversation.

---

## 1. What We Are Building (in one sentence)

An AI-first Vedic Astrology & Numerology website: a customer signs up, enters their birth details once, gets an accurately calculated Kundli (birth chart) with a plain-language life summary, and then can chat with an AI assistant that answers personal questions about their own chart — using real calculated data, not guesses.

## 2. Why We're Building It This Way

- We do **not** want "just another Kundli generator." The point of difference is the **AI assistant** on top of a real, saved chart.
- We do **not** want to build the whole astrology universe on day one — Dasha, Yogas, transits, divisional charts, numerology all come **later**, in phases, on top of the same foundation.
- The AI must **never invent or guess** planetary positions or chart facts. Facts always come from a real calculation engine/API; the AI's job is only to explain those facts using trusted knowledge (RAG) and conversation.

## 3. What We Already Decided

| Decision | Choice |
|---|---|
| Who can use it (Phase 1) | Public — anyone can sign up themselves (not just you entering clients manually) |
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python + FastAPI + SQLAlchemy + Pydantic |
| Database | PostgreSQL (permanent storage of users, profiles, charts, chat history) |
| Astrology calculation source | Prokerala Astrology API as primary (accurate, well-documented, Swiss-Ephemeris based) — built behind an internal interface so it can be swapped; also evaluate VedAstro and Rajvidya since they bundle Dasha/Yoga/numerology and might reduce how many separate APIs we need later |
| Knowledge base for AI | RAG (pgvector + PostgreSQL) built from legally usable classical astrology texts + our own notes — never scraped/copied copyrighted modern books |
| AI style | LLM + tool-calling + RAG (grounded), **not** fine-tuning, at least for now |
| Visual style | Cute, soft, feminine, modern — light blue as main colour, with white/soft pink/lavender/light blue-grey as support colours |
| Admin/astrologer dashboard ("My Clients") | Designed for later — database is built so this can be added without rebuilding, but not part of Phase 1 UI |
| Numerology | Same architecture as astrology (deterministic calculation → stored in DB → explained via RAG + LLM), but a later phase, not Phase 1 |

## 4. The Core Product Flow (Phase 1 — what we build first)

```
Customer signs up
   → Enters birth details (name, gender, DOB, exact birth time, birth place)
   → System resolves birth place into latitude, longitude, timezone
   → Backend sends details to the astrology calculation API
   → Chart is calculated (Lagna, Rashi, planets, signs, houses, degrees)
   → Everything is saved permanently in PostgreSQL
   → Customer sees their Kundli dashboard + simple personality/career/love/money summary
   → Customer chats with the AI about their exact chart
   → Everything reloads instantly next time they log in — nothing is re-entered
```

## 5. What Is Deliberately NOT in Phase 1

These are real, planned, but come in **later phases** so we don't try to build everything at once:

- Nakshatra, Pada, Retrograde, Combust, Exalted, Debilitated, Vargottama, Aspects (Phase 2)
- Deeper personality/career/love/money analysis (Phase 3)
- Vimshottari Dasha / Antardasha (Phase 4)
- Yogas / Rajyogas (Phase 5)
- Divisional charts — D9/Navamsa, D10, etc. (Phase 6)
- Transits + personalized astrology calendar (Phase 7)
- Full agentic AI ("what's happening in my chart right now" combining everything) (Phase 8)
- Numerology (parallel track, after Phase 1 is stable)
- Astrologer/Admin "My Clients" dashboard (parallel track, after Phase 1 is stable)
- Payments, native mobile apps, chart comparison/compatibility — not yet scoped

## 6. The Architecture, in Plain Words

Think of it as five separate specialists working together, instead of one giant AI that "knows everything":

1. **Astrology Engine/API** — does the actual math. Facts only.
2. **PostgreSQL Database** — remembers every customer, their chart, and every conversation, forever.
3. **RAG Knowledge Base** — holds the trusted astrology books/notes the AI is allowed to quote from.
4. **LLM (the AI brain)** — understands the customer's question, decides what tool or knowledge to pull, and explains it warmly.
5. **React Website** — the pretty, soft, easy-to-use front door for the customer.

Rule that never changes as we add phases: **the AI explains calculations, it never invents them.**

## 7. Final Outcome — What "Done" Looks Like for Phase 1

> A new visitor signs up, enters their birth details once, immediately sees an accurately calculated Kundli with a simple, plain-language personality/career/love/money summary, can ask the AI natural questions about that exact chart and get answers grounded in real chart data and cited astrology knowledge, and when they come back later — everything (chart + full chat history) is exactly as they left it, with nothing to re-enter.

## 8. Where Things Live

- `docs/PRD.md` — full detailed product requirements (data model, API structure, tech stack, tools list, etc.)
- `planning/PROJECT_PLAN.md` — this file, the plain-language running summary of what we've planned and decided
- `backend/` — FastAPI backend (to be built)
- `frontend/` — React frontend (to be built)

## 9. What's Next

Once you're ready, the next step is turning this plan into actual code: a FastAPI backend skeleton (database models, the astrology-provider connector, the AI agent + tools), a React frontend skeleton (sign-up/login, birth details form, Kundli dashboard, AI chat), and the PostgreSQL schema/migrations — all following exactly what's written above so nothing here is rebuilt later.
