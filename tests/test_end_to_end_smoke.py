# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""End-to-end smoke: run_one_step returns FinalDecision, PacketV2, and optional Report."""

from harness import run_one_step


def test_run_one_step_returns_three_values() -> None:
    """run_one_step(state, context, now_ms) returns (FinalDecision, PacketV2, report)."""
    state = {"signal_0": 0.5, "signal_1": 0.0, "state_scalar_a": 0.0}
    context = {}
    now_ms = 1700000000000
    final_decision, packet, report = run_one_step(
        state, context, now_ms, run_id="smoke", step=0
    )
    assert final_decision is not None
    assert hasattr(final_decision, "action") and hasattr(final_decision, "allowed")
    assert packet is not None
    assert packet.run_id == "smoke"
    assert packet.step == 0
    assert packet.latency_ms >= 0
    assert packet.schema_version
    # report may be None if eval-calibration-core not installed
    if report is not None:
        assert hasattr(report, "suite_name")
