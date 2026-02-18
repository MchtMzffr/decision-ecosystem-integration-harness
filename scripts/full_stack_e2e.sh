#!/usr/bin/env bash
# Full-stack E2E: venv + install [dev,full] + run fullstack tests.
# Usage: ./scripts/full_stack_e2e.sh  (from repo root)
set -e
cd "$(dirname "$0")/.."
python -m venv .venv
# shellcheck source=/dev/null
. .venv/bin/activate
pip install -U pip
pip install -e ".[dev,full]"
pytest tests/ -m fullstack -v
