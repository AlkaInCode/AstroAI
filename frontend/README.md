# AstroAI Frontend

React + Vite + Tailwind CSS frontend for Phase 1.

## Setup

```bash
npm install
npm run dev
```

Runs at `http://localhost:5173`. API calls to `/api/*` are proxied to the backend at
`http://localhost:8000` (see `vite.config.js`) — run the backend alongside this.

## Pages

- `/` — landing page
- `/signup`, `/login` — auth
- `/create-profile` — birth details form (protected)
- `/dashboard` — redirects to the customer's existing Kundli, or to profile creation if they have none
- `/dashboard/:profileId` — Kundli chart, planet table, life-area summary, AI chat (protected)

## Notes

- Birth place search uses OpenStreetMap Nominatim (free, no API key) for real city lookup.
  Timezone is a manual picker with a rough auto-guess from longitude — replace with a real
  geocoding+timezone provider when one is chosen for production (see backend README).
- Auth token is stored in `localStorage` and sent as a Bearer token on every API call.
- Tailwind theme colors (light blue / pink / lavender) are defined in `src/index.css`.
