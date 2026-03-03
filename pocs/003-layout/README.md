# 003 — Anza SolarPro

A solar farm layout design tool. Draw land boundaries, place keepout zones, auto-fill with rack rectangles, and run a stochastic optimizer to find the highest kW DC layout across all rack and module combinations.

---

## Prerequisites

- Node.js (install via `brew install node`)
- A free [Supabase](https://supabase.com) account

---

## Setup

### 1. Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor → New Query**, paste the contents of `supabase/migrations/001_initial.sql`, and click **Run**
3. Go to **Authentication → Providers → Email** and disable "Confirm email" (easier for testing)
4. Go to **Settings → API** and copy your **Project URL** and **anon public key**

### 2. Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Install & Run

```bash
npm install
npm run dev
```

Opens at [http://localhost:5173](http://localhost:5173)

---

## User Journey

1. **Register** — create an account. A default module and rack library is automatically seeded.
2. **Create a project** — name, optional address, and GPS coordinates (right-click any location on Google Maps to copy lat/lng).
3. **Open the map** — draw a boundary polygon around the usable land.
4. Set a **perimeter offset** to shrink the usable area inward (setback requirements).
5. Draw **keepout zones** for roads, trees, or buildings. Each has its own buffer offset.
6. Select a **rack type** and **PV module** from the library.
7. Set **N/S spacing** (or GCR — bidirectionally linked) and **E/W spacing**.
8. Click **Fill** — racks are packed into the usable area. Live stats show rack count and kW DC.
9. Click **Save & Exit** to persist. Reopening a project fully restores the layout.
10. Click **Evaluate** — 100 spacing-perturbation trials per rack × module combination. Results table sorted by kW DC. Hover a row to see the kW DC histogram.
11. Click a result row to return to the map with that layout applied.
12. **Edit Layout** on any row to manually tweak spacing and save as a **Custom Layout**.

---

## Pages

| Page | Route | Purpose |
|---|---|---|
| Login | `/login` | Sign in / sign up |
| Projects | `/` | Create and manage projects |
| Project Map | `/projects/:id/map` | Design workspace |
| Evaluate | `/projects/:id/evaluate` | Optimizer results |
| Modules | `/modules` | PV module library (CRUD) |
| Racking | `/racks` | Rack type library (CRUD) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS v4 + shadcn/ui |
| Map | Leaflet.js + leaflet-draw |
| Geo math | Turf.js |
| Charts | Recharts |
| Backend / Auth / DB | Supabase (Postgres + RLS) |

---

## Notes

- All compute (fill algorithm, optimizer) runs in the browser — no server needed beyond Supabase.
- Rack positions are not persisted; they are regenerated from boundary + spacing params on load.
- The optimizer is synchronous. With 5 racks × 10 modules × 100 trials = 5,000 fill runs, expect 2–5 seconds.
