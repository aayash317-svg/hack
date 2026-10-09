#!/bin/bash
# Campus Safety & Harassment Reporting System - Database Seeder
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "backend/.venv/bin/python" ]; then
    PYTHON_EXEC="backend/.venv/bin/python"
elif [ -f "backend/.venv/bin/python3" ]; then
    PYTHON_EXEC="backend/.venv/bin/python3"
elif command -v python3 &>/dev/null; then
    PYTHON_EXEC="python3"
else
    echo "Error: Python 3 not found."
    exit 1
fi

exec "$PYTHON_EXEC" database/seeds/seed_demo.py
