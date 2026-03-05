# AGENTS.md

## Cursor Cloud specific instructions

This is an AI Multi-Agent Supply Chain Optimizer with a **FastAPI backend** (port 8000) and a **Next.js frontend** (port 3000). The system works fully offline with mock/computed data — no external API keys are required.

### Services

| Service | Port | Start command |
|---------|------|---------------|
| Backend | 8000 | `cd /workspace/backend && source venv/bin/activate && python main.py` |
| Frontend | 3000 | `cd /workspace/frontend && npm run dev` |

### Key caveats

- **python3.12-venv** must be installed via apt before creating the virtualenv (`sudo apt-get install -y python3.12-venv`). The update script handles this.
- The `npm run lint` script in `frontend/package.json` references ESLint, but no `eslint.config.*` file exists in the repo. The lint command will fail; this is a pre-existing issue.
- TypeScript strict checking (`npx tsc --noEmit`) shows pre-existing type errors in `vendor-routes.tsx` and `chart.tsx`. The app still builds and runs fine via `npm run dev`.
- CrewAI is optional and commented out in `requirements.txt`. The backend gracefully falls back to computational-only analysis.
- Backend `.env` and frontend `.env.local` are not checked into git. Create them if missing:
  - `backend/.env`: empty API keys are fine (all have fallbacks)
  - `frontend/.env.local`: needs `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Backend health check: `curl http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- To test core flow: `POST /api/analyze` with `{"origin":"Mumbai","destination":"Delhi","scenario":"normal"}`
