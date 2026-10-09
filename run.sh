#!/bin/bash
# Campus Safety & Harassment Reporting System - Dev Runner
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
    echo "Error: Python 3 not found. Please ensure backend/.venv is set up."
    exit 1
fi

echo "🛡️  Starting Campus Safety & Harassment Reporting System..."
echo "📍 Local Web & API: http://localhost:8000"
echo "🌐 Public Tunnel:   https://progressive-chronic-authorization-hey.trycloudflare.com"

exec "$PYTHON_EXEC" -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
