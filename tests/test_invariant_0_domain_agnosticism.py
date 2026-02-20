# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INVARIANT 0: Domain-agnosticism in public surface (README + docs, excluding examples).

Scans README.md and docs/ (excluding docs/examples). Harness code and examples may
use domain-agnostic generic keys (signal_0, state_scalar_a, etc.); this test locks doc drift.
"""

import re
from pathlib import Path

FORBIDDEN_TERMS = {
    "trade",
    "trading",
    "trader",
    "market",
    "orderbook",
    "bid",
    "ask",
    "quote",
    "fill",
    "exchange",
    "portfolio",
    "pnl",
    "slippage",
    "spread",
    "liquidity",
    "inventory",
    "exposure",
    "drawdown",
    "flatten",
    "cancel_all",
    "mid",
    "imbalance",
    "depth",
    "spread_bps",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DOCS = ["README.md", "docs/"]
EXCLUDE = [r"docs[/\\]examples[/\\]"]


def _find_files() -> list[Path]:
    files = []
    for p in PUBLIC_DOCS:
        path = REPO_ROOT / p
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
        else:
            for f in path.rglob("*"):
                if f.is_file() and f.suffix in (".md", ".rst", ".txt"):
                    rel = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
                    if not any(re.search(pat, rel, re.IGNORECASE) for pat in EXCLUDE):
                        files.append(f)
    return files


def test_invariant_0_docs_domain_agnostic() -> None:
    """README and docs (excluding docs/examples) must not contain domain vocabulary."""
    violations = []
    for f in _find_files():
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            lower = line.lower()
            for term in FORBIDDEN_TERMS:
                if term in lower and not line.strip().startswith("#"):
                    violations.append((str(f.relative_to(REPO_ROOT)), i, term))
    assert not violations, "INVARIANT 0 (docs) violated: " + str(violations[:15])
