#!/usr/bin/env bash
set -e
trap "kill 0" EXIT
(cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000) &
(cd frontend && npm run dev -- --port 3000) &
wait
