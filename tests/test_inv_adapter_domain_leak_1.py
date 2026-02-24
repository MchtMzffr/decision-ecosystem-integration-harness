# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-ADAPTER-DOMAIN-LEAK-1: Adapter module names must have example_domain_ prefix."""

import pkgutil
from pathlib import Path


def test_inv_adapter_domain_leak_1_no_bare_domain_modules() -> None:
    """Adapter modules (except base, __init__) must be named example_domain_* (INV-ADAPTER-DOMAIN-LEAK-1)."""
    import harness.platform.adapters as pkg

    adapters_path = Path(pkg.__file__).resolve().parent
    allowed_bare = {"base", "__init__"}
    for mod in pkgutil.iter_modules([str(adapters_path)]):
        name = mod.name
        if name in allowed_bare:
            continue
        assert name.startswith(
            "example_domain_"
        ), f"Adapter module must have example_domain_ prefix: {name}"
