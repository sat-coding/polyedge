# PolyEdge — AI-Powered Polymarket Trading Bot

Monorepo with:
- **backend/** FastAPI service (scanner, signals, portfolio, paper execution)
- **frontend/** Next.js dashboard
- **scripts/** local dev and tunnel helpers

## Quick start

```bash
cp .env.example .env
make dev
```

Backend: `http://127.0.0.1:8000`
Frontend: `http://127.0.0.1:3000`

## Notes
- Default is **paper mode** (no real orders)
- OpenAI integration is optional via `OPENAI_API_KEY`
