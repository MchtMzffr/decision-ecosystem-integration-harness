# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Tests for platform: catalog, store, control."""

from harness import (
    clear_memory_buffer,
    clear_ops_override,
    get_context_overrides,
    get_memory_buffer,
    get_ops_state,
    merge_context,
    set_green,
    set_red,
    store_save,
)
from decision_schema.packet_v2 import PacketV2


def test_catalog_get_context_overrides_empty() -> None:
    """Without env, overrides are empty (or only from DECISION_* if set)."""
    overrides = get_context_overrides()
    assert isinstance(overrides, dict)


def test_catalog_merge_context() -> None:
    """merge_context merges overrides into base."""
    base = {"now_ms": 1000, "run_id": "r1"}
    overrides = {"ops_state": "RED"}
    out = merge_context(base, overrides)
    assert out["now_ms"] == 1000
    assert out["ops_state"] == "RED"


def test_control_set_red_green() -> None:
    """set_red / set_green update ops state."""
    clear_ops_override()
    set_red()
    state = get_ops_state()
    assert state.get("ops_deny_actions") is True
    assert state.get("ops_state") == "RED"
    set_green()
    state = get_ops_state()
    assert state.get("ops_deny_actions") is False
    assert state.get("ops_state") == "GREEN"
    clear_ops_override()


def test_store_memory() -> None:
    """save with backend=memory appends to buffer when packet has harness.redaction_applied (INV-STORE-SEC-1)."""
    clear_memory_buffer()
    packet = PacketV2(
        run_id="r1",
        step=0,
        input={},
        external={"harness.redaction_applied": True},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": True, "reasons": []},
        latency_ms=1,
    )
    store_save(packet, report=None, backend="memory")
    buf = get_memory_buffer()
    assert len(buf) == 1
    assert buf[0]["packet"]["run_id"] == "r1"
    clear_memory_buffer()
