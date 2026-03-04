# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

AI Multi-Agent Logistics Optimizer — a FastAPI (Python) backend + Next.js 16 (TypeScript) frontend. No database required; all data is mock/in-memory. External API keys (OpenAI, Google Maps, WeatherAPI) are optional with graceful fallbacks.

### Services

| Service | Port | Command |
|---------|------|---------|
| Backend (FastAPI) | 8000 | `cd backend && uvicorn main:app --reload --port 8000` |
| Frontend (Next.js) | 3000 | `cd frontend && npm run dev` |

Both services must run for end-to-end testing. Start the backend first since the frontend proxies API requests to it via `next.config.mjs` rewrites.

### Key caveats

- **PATH**: `~/.local/bin` must be on `PATH` for `uvicorn` and other pip-installed CLI tools. This is already configured in `~/.bashrc`.
- **Frontend `.env.local`**: Must exist at `frontend/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`. Created automatically during setup; if missing, copy from `frontend/.env.example`.
- **ESLint**: The `npm run lint` script references `eslint` but ESLint is not listed as a project dependency and no config file exists. `npm run lint` will fail — this is a pre-existing project gap, not an environment issue.
- **TypeScript errors**: Pre-existing TS errors exist in `components/pages/vendor-routes.tsx` and `components/ui/chart.tsx`. The build succeeds because `next.config.mjs` sets `typescript.ignoreBuildErrors: true`.
- **pip install is slow**: `requirements.txt` pulls in heavy packages (torch, sentence-transformers, chromadb). Initial install takes ~2 minutes.
- **Backend dependencies use system Python**: Dependencies are installed globally via `pip install` (no venv), matching the cloud VM setup pattern.
- For standard dev commands (build, test, start), see `README.md > Quick Start` and `package.json` scripts.
