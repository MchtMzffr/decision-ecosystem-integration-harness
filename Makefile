# Release recipe: core-only, full-stack, and combined test targets.
# Requires: Python 3.11+, pip, pytest

.PHONY: core full all

core:
	pytest tests/ -m "not fullstack" -v

full:
	pytest tests/ -m fullstack -v

all: core full
