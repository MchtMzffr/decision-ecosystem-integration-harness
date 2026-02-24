# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-README-NO-PLACEHOLDER-1: README has no license placeholder. Schema pin >=0.2.2."""

from pathlib import Path


def test_inv_readme_no_placeholder_1_license() -> None:
    """README must not contain '[Add your license]' (INV-README-NO-PLACEHOLDER-1)."""
    root = Path(__file__).resolve().parent.parent
    readme = root / "README.md"
    assert readme.exists(), "README.md missing"
    text = readme.read_text(encoding="utf-8")
    assert (
        "[Add your license]" not in text
    ), "INV-README-NO-PLACEHOLDER-1: Remove license placeholder from README"


def test_inv_readme_schema_pin_0_2_2() -> None:
    """README schema dependency must pin >=0.2.2 (ecosystem standard)."""
    root = Path(__file__).resolve().parent.parent
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert (
        "0.2.2" in text and "decision-schema" in text
    ), "README must document decision-schema pin >=0.2.2 (e.g. >=0.2.2,<0.3)"
