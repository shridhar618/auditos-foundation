# AuditOS — Foundation Build (Phase 1)

Autonomous Enterprise Audit & Compliance Intelligence Platform.
This is Phase 1 of the feature-by-feature build: **architecture, database schema,
project scaffold, and Authentication + RBAC.** Everything here is real, working
code — not placeholders — but the business modules (dashboard data, investigations,
AI agents, etc.) are stubbed as "coming soon" pages until their own build phase.

## Architecture decisions (Step 1–3 of the workflow)

- **Backend**: FastAPI + SQLAlchemy 2.0, Clean/DDD-ish layering:
  - `app/domain/models` — ORM entities only, no business logic
  - `app/repositories` — Repository Pattern; all raw queries live here
  - `app/services` — business rules and orchestration (the only layer that
    raises domain exceptions)
  - `app/api/v1` — thin HTTP routers that translate request ↔ service call
  - `app/core` — config, DB engine, JWT/password utilities, domain exceptions
- **Multi-tenancy**: every business table carries `organization_id`. A user
  only ever sees data scoped to their own organization.
- **RBAC**: granular `resource:action` permissions (e.g. `investigations:approve`)
  bundled into roles (`admin`, `compliance_officer`, `auditor`, `viewer`).
  Enforced declaratively per-route via `Depends(require_permission("code"))`.
- **Auth**: short-lived JWT access tokens (15 min) + longer-lived, rotating,
  revocable refresh tokens (7 days) persisted in `refresh_tokens` so logout /
  admin-forced logout actually works (not just relying on JWT expiry).
- **Frontend**: React + TypeScript + Vite + Tailwind, shadcn-style component
  primitives (hand-written, no CLI needed), TanStack Query for server state,
  React Hook Form + Zod for forms, Framer Motion for polish, dark/light theme
  via CSS variables.

## Prerequisites

- Docker + Docker Compose (recommended path), **or**
- Python 3.12+, Node.js 20+, a local PostgreSQL 16 and Redis 7 if running without Docker

## Quick start (Docker — recommended)

```bash
# 1. Copy env template and edit as needed (JWT secret especially)
cp backend/.env.example backend/.env

# 2. Build and start everything
docker compose up --build

# 3. In a second terminal, run migrations and seed roles/permissions
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed
```

- Frontend: http://localhost:5173
- Backend docs (Swagger): http://localhost:8000/api/docs
- Health check: http://localhost:8000/api/health

Open the frontend, click **"Create your organization"**, and register — this
creates your tenant plus your first `admin` user with every permission.

## Quick start (without Docker)

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # edit DATABASE_URL to point at your local Postgres

alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Project layout

```
auditos/
├── backend/
│   ├── app/
│   │   ├── core/            # config, db, security, exceptions
│   │   ├── domain/models/    # SQLAlchemy entities
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── repositories/     # data access layer
│   │   ├── services/         # business logic
│   │   ├── api/v1/           # routers
│   │   ├── main.py
│   │   └── seed.py           # seeds default roles + permission catalogue
│   ├── alembic/               # migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/{ui,layout}/
│   │   ├── context/           # Auth + Theme providers
│   │   ├── lib/                # api client, validation, utils
│   │   ├── pages/
│   │   ├── routes/             # ProtectedRoute
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## What's next (per the feature-by-feature roadmap)

1. **Dashboard module** — real KPIs, compliance/risk scores, trend charts (Recharts)
2. **Transaction Management** — ingestion, listing, detail views
3. **AI Agent pipeline** — Supervisor → Detection → Policy → Investigation → Evidence
   → Recommendation, built with LangGraph, with human-approval gates
4. **Document & Policy Center** — upload, OCR, pgvector semantic search
5. **Reporting & Analytics** — PDF/Excel export, heatmaps, risk matrix

Each phase follows: understand → design architecture → design DB → design API →
design UI → implement backend → implement frontend → integrate AI → test → refactor,
same as this one.
