.PHONY: setup dev backend frontend tunnel test
setup:
	bash scripts/setup.sh

dev:
	bash scripts/dev.sh

backend:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

frontend:
	cd frontend && npm run dev -- --port 3000

tunnel:
	bash scripts/tunnel.sh

test:
	cd backend && . .venv/bin/activate && pytest tests -v
