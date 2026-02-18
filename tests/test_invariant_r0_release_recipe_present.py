# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT R0: Release recipe assets exist (script + doc) so CI/local gate does not drift."""

from pathlib import Path


def test_inv_r0_full_stack_e2e_script_exists() -> None:
    """scripts/full_stack_e2e.sh must exist."""
    root = Path(__file__).resolve().parent.parent
    script = root / "scripts" / "full_stack_e2e.sh"
    assert script.is_file(), "scripts/full_stack_e2e.sh required for release recipe"


def test_inv_r0_release_recipe_doc_exists() -> None:
    """docs/RELEASE_RECIPE.md must exist."""
    root = Path(__file__).resolve().parent.parent
    doc = root / "docs" / "RELEASE_RECIPE.md"
    assert doc.is_file(), "docs/RELEASE_RECIPE.md required for release recipe"


def test_inv_r0_makefile_has_core_full_all() -> None:
    """Makefile must define core, full, all targets."""
    root = Path(__file__).resolve().parent.parent
    makefile = root / "Makefile"
    assert makefile.is_file(), "Makefile required for release recipe"
    content = makefile.read_text()
    assert "core:" in content
    assert "full:" in content
    assert "all:" in content
