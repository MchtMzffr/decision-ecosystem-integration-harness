# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-V1: Version single-source - pyproject version must match package __version__."""

import tomllib
from pathlib import Path

import harness


def test_version_single_source() -> None:
    """pyproject.toml version must equal harness.__version__ (no drift)."""
    repo_root = Path(__file__).resolve().parent.parent
    with (repo_root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    pyproject_version = data["project"]["version"]
    assert harness.__version__ == pyproject_version, (
        "Version drift: pyproject.toml has %r, harness.__version__ is %r"
        % (pyproject_version, harness.__version__)
    )
