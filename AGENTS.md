# AGENTS.md

Productivity app ("SYFU") with a LangChain/LangGraph agent backend and a Vue 3 frontend. Two independent subprojects, no root config, no CI.

## Layout

- `backend/` — Python 3.14, FastAPI + LangChain/LangGraph + SQLAlchemy. Managed with **uv** (venv at `backend/.venv`).
- `frontend/` — Vue 3 + TypeScript + Vite + Tailwind v4. Managed with **bun**.
- `backend/rag/test/` — scratch area: Jupyter notebooks, sample docs, committed Chroma DB and a test `main.db`. Experimentation, not product code. Real app code lives in `backend/src/syfu/`.
- `backend/main.py` and `backend/extensions.py` are empty decoys; the real entrypoint is `backend/src/syfu/main.py`.

## Backend

- Package is `syfu` under a `src/` layout: `api/routers/` (FastAPI), `core/db.py` (engine + `init_db()`), `models/` (SQLAlchemy), `schemas/` (Pydantic), `tools/` (LangChain tools), `prompts/`. The project is a hatchling src-layout package (`[tool.hatch.build.targets.wheel] packages = ["src/syfu"]`) — after a fresh clone run `uv sync` in `backend/` before anything else. All imports use the `syfu.*` form; don't introduce `src.syfu.*`.
- Run the API from `backend/`: `uv run python -m syfu.main` → serves `0.0.0.0:8000`, only `/api/health` exists.
- No tests, lint, or formatter configured. Verify by running the server and hitting `/api/health`.
- SQLite DB: `backend/main.db` (untracked, gitignored-looking but not in .gitignore — don't commit it). Path is derived from `src/syfu/core/db.py` (`parents[3] / "main.db"`). Tables are created by `init_db()`, which is wired into the FastAPI lifespan (startup), so they auto-create on boot. `backend/rag/test/main.db` is a separate scratch DB.
- `backend/.env` holds real GROQ/NVIDIA API keys (gitignored). Notebooks and agent code read them via `load_dotenv()`; they're required for LLM/embedding calls.
- Notebooks in `backend/rag/test/` must run with cwd=`backend/rag/test`: they use relative paths (`./docs`, `./info`, `./Chroma`) and append `src/` (not the backend root) to `sys.path`. The current agent prototype uses `ChatGroq(llama-3.1-8b-instant)` + `NVIDIAEmbeddings(nemotron-3-embed-1b)`; the state graph lives in `tooling.ipynb`.

## Frontend

- Commands (from `frontend/`): `bun install`, `bun dev`, `bun run build` (`vue-tsc -b && vite build`), `bun run preview`. No lint/test configured.
- Router uses `createMemoryHistory()` in `src/main.ts` — `/dashboard` is routed but the app mounts `Landing` at root regardless of URL.
- Tailwind v4 is CSS-first: no `tailwind.config.*`; config lives in `src/style.css` via `@import "tailwindcss"`. Fonts (Sora, Space Grotesk) come from `@fontsource` imports in `main.ts` with helper classes `.sora`/`.space`.
- No backend integration yet — no API proxy, no `VITE_*` env.
