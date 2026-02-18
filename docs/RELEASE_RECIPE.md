# Release Recipe (single-command verification)

Before cutting a release, run the following to verify the integration harness and ecosystem contract.

## One-command check

**Option A — Make (recommended)**

```bash
make all
```

Runs `make core` then `make full`. Expected: `X passed, 0 failed, 0 skipped` for both.

**Option B — Script (full-stack only)**

```bash
./scripts/full_stack_e2e.sh
```

Creates `.venv`, installs harness with `[dev,full]`, runs fullstack tests. Use from repo root (e.g. Git Bash or WSL on Windows).

**Option C — Manual**

```bash
pip install -e ".[dev,full]"
pytest tests/ -v
```

## Targets (Makefile)

| Target | Command | Meaning |
|--------|---------|---------|
| `make core` | `pytest tests/ -m "not fullstack" -v` | Core-only tests (no optional cores required) |
| `make full` | `pytest tests/ -m fullstack -v` | Full-stack tests (mdm-engine, dmc-core, ops-health-core, evaluation-calibration-core) |
| `make all` | core then full | Full release gate |

## Expected outcomes

- **INV-R1:** full_stack job → `0 failed`
- **INV-R2:** In full-stack runs, `report.contract_matrix_check["compatible"] is True` (asserted in `test_fullstack_e2e_report.py`)

## CI

GitHub Actions already runs `core_only` and `full_stack` jobs; this recipe mirrors that gate locally so you can validate before push.
