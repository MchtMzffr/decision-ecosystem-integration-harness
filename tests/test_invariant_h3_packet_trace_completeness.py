# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT H3: PacketV2 trace completeness — required fields present and non-empty."""

from decision_schema.types import Action, FinalDecision, Proposal

from harness.packet_builder import build_packet_v2

REQUIRED_PACKET_V2_FIELDS = (
    "run_id",
    "step",
    "input",
    "external",
    "mdm",
    "final_action",
    "latency_ms",
    "schema_version",
)


def test_packet_v2_required_fields_present() -> None:
    """PacketV2 must have all required fields (PARAMETER_INDEX)."""
    proposal = Proposal(action=Action.ACT, confidence=0.7, reasons=[])
    final = FinalDecision(action=Action.ACT, allowed=True, reasons=[])
    packet = build_packet_v2(
        run_id="r1",
        step=0,
        input_snapshot={"a": 1},
        external_snapshot={"now_ms": 0},
        proposal=proposal,
        final_decision=final,
        latency_ms=10,
        mismatch=None,
    )
    d = packet.to_dict()
    for key in REQUIRED_PACKET_V2_FIELDS:
        assert key in d, f"Missing required field: {key}"
        if key in ("run_id", "schema_version"):
            assert d[key], f"Required field must be non-empty: {key}"
        elif key == "input":
            assert isinstance(d[key], dict), "input must be dict"
        elif key == "external":
            assert isinstance(d[key], dict), "external must be dict"
        elif key == "mdm":
            assert isinstance(d[key], dict), "mdm must be dict"
        elif key == "final_action":
            assert isinstance(d[key], dict), "final_action must be dict"


def test_packet_v2_schema_version_non_empty() -> None:
    """schema_version must be set (from decision_schema)."""
    proposal = Proposal(action=Action.HOLD, confidence=0.0, reasons=[])
    final = FinalDecision(action=Action.HOLD, allowed=True, reasons=[])
    packet = build_packet_v2(
        run_id="r2",
        step=1,
        input_snapshot={},
        external_snapshot={},
        proposal=proposal,
        final_decision=final,
        latency_ms=0,
    )
    assert packet.schema_version and len(packet.schema_version) > 0
