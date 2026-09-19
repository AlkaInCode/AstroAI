# AstroAI Frontend

React + Vite + Tailwind CSS frontend.

Prefer running this via `docker compose up --build` from the repo root (see the top-level README) unless you specifically need to run it natively.

## Setup

```bash
npm install
npm run dev
```

Runs at `http://localhost:5173`. API calls to `/api/*` are proxied to the backend (`http://localhost:8000` by default,
or `VITE_BACKEND_URL` if set — see `vite.config.js`) — run the backend alongside this.

## Pages

- `/` — landing page
- `/signup`, `/login` — auth
- `/create-profile` — birth details form (protected)
- `/dashboard` — routes to the customer's one Kundli, the clients list if they have several, or profile creation if they have none
- `/dashboard/:profileId` — Kundli chart, planet table, life-area summary, Dasha timeline, Yogas, divisional charts, transits, numerology, AI chat (protected)
- `/clients` — searchable list of all birth profiles under the account, with inline rename and delete (protected)
- `/settings` — bring-your-own LLM API key (protected)

## Notes

- Birth place search uses OpenStreetMap Nominatim (free, no API key) for real city lookup.
  Timezone is a manual picker with a rough auto-guess from longitude — replace with a real
  geocoding+timezone provider when one is chosen for production (see backend README).
- Auth token is stored in `localStorage` and sent as a Bearer token on every API call.
- Tailwind theme colors (light blue / pink / lavender) are defined in `src/index.css`.
