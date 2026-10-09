#!/bin/bash
# Campus Safety & Harassment Reporting System - Automated Test Runner
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "backend/.venv/bin/pytest" ]; then
    PYTEST_EXEC="backend/.venv/bin/pytest"
elif command -v pytest &>/dev/null; then
    PYTEST_EXEC="pytest"
else
    echo "Error: pytest not found. Please ensure backend/.venv is set up."
    exit 1
fi

exec "$PYTEST_EXEC" backend/tests/ -v "$@"
