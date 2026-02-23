# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-STORE-SEC-1 and INV-STORE-NO-PII-1: Store redaction gate and secret pattern refusal."""

from decision_schema.packet_v2 import PacketV2

from harness.platform.store import clear_memory_buffer, get_memory_buffer, save


def test_inv_store_sec_1_redaction_required() -> None:
    """Without harness.redaction_applied=True in packet.external, store does not write (INV-STORE-SEC-1)."""
    clear_memory_buffer()
    packet = PacketV2(
        run_id="r1",
        step=0,
        input={},
        external={},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": True, "reasons": []},
        latency_ms=1,
    )
    save(packet, report=None, backend="memory")
    buf = get_memory_buffer()
    assert len(buf) == 0
    clear_memory_buffer()


def test_inv_store_sec_1_redaction_applied_writes() -> None:
    """With harness.redaction_applied=True, store writes."""
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
    save(packet, report=None, backend="memory")
    buf = get_memory_buffer()
    assert len(buf) == 1
    clear_memory_buffer()


def test_inv_store_no_pii_1_token_pattern_fails() -> None:
    """Payload containing secret-like pattern is not written (INV-STORE-NO-PII-1)."""
    clear_memory_buffer()
    packet = PacketV2(
        run_id="r1",
        step=0,
        input={"leak": "sk-abc12345678901234567890"},
        external={"harness.redaction_applied": True},
        mdm={"action": "HOLD"},
        final_action={"action": "HOLD", "allowed": True, "reasons": []},
        latency_ms=1,
    )
    save(packet, report=None, backend="memory")
    buf = get_memory_buffer()
    assert len(buf) == 0
    clear_memory_buffer()
