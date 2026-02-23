# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-ADAPTER-REG-1: Every registry adapter importable and implements BaseAdapter. INV-ADAPTER-DET-1: Same input -> same (state, context) order-stable."""

import json

from harness.platform.adapters import get_adapter
from harness.platform.adapters.base import BaseAdapter


# SSOT: adapter names that must be in registry (INV-ADAPTER-REG-1).
_ADAPTER_NAMES = (
    "example_domain_agent_tool_use",
    "example_domain_content_moderation",
    "example_domain_lending",
    "example_domain_ops_automation",
    "example_domain_scheduling",
    "example_domain_triage",
    "example_domain_trading",
)


def test_inv_adapter_reg_1_importable_and_type() -> None:
    """Every name in registry returns an instance that is a BaseAdapter (INV-ADAPTER-REG-1)."""
    for name in _ADAPTER_NAMES:
        adapter = get_adapter(name)
        assert isinstance(adapter, BaseAdapter), f"{name} must be BaseAdapter instance"


def test_inv_adapter_det_1_stable_mapping() -> None:
    """Same domain_input -> same (state, context) when serialized to order-stable JSON (INV-ADAPTER-DET-1)."""
    for name in _ADAPTER_NAMES:
        adapter = get_adapter(name)
        domain_input = {"x": 1, "y": "a", "z": [1, 2]}
        state1, ctx1 = adapter.to_state_context(domain_input)
        state2, ctx2 = adapter.to_state_context(domain_input)
        assert json.dumps(state1, sort_keys=True) == json.dumps(
            state2, sort_keys=True
        ), f"{name} state not deterministic"
        assert json.dumps(ctx1, sort_keys=True) == json.dumps(ctx2, sort_keys=True), (
            f"{name} context not deterministic"
        )
