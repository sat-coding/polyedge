#!/usr/bin/env bash
set -e
cd backend
python3.13 -m venv .venv
. .venv/bin/activate
pip install -q -e .
cd ../frontend
npm install --silent
cd ..
python backend/app/database.py
echo "setup done"
