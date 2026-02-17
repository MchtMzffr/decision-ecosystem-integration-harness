"""Build PacketV2 from proposal, final decision, and context (PARAMETER_INDEX-aligned)."""

from __future__ import annotations

import time
from typing import Any

from decision_schema.packet_v2 import PacketV2
from decision_schema.types import Action, FinalDecision, Proposal

from harness.redaction import redact_dict


def build_packet_v2(
    run_id: str,
    step: int,
    input_snapshot: dict[str, Any],
    external_snapshot: dict[str, Any],
    proposal: Proposal,
    final_decision: FinalDecision,
    latency_ms: int,
    mismatch: dict[str, Any] | None = None,
    redact_input: bool = True,
    redact_external: bool = True,
) -> PacketV2:
    """
    Build PacketV2 with required fields (run_id, step, input, external, mdm, final_action, latency_ms, schema_version).
    Input/external are redacted by default for safe tracing.
    """
    input_ = redact_dict(input_snapshot) if redact_input else dict(input_snapshot)
    external = redact_dict(external_snapshot) if redact_external else dict(external_snapshot)
    mdm = _proposal_to_mdm_dict(proposal)
    final_action = _final_decision_to_dict(final_decision)
    return PacketV2(
        run_id=run_id,
        step=step,
        input=input_,
        external=external,
        mdm=mdm,
        final_action=final_action,
        latency_ms=latency_ms,
        mismatch=mismatch,
    )


def _proposal_to_mdm_dict(p: Proposal) -> dict[str, Any]:
    return {
        "action": p.action.value,
        "confidence": p.confidence,
        "reasons": list(p.reasons),
        "params": (p.params or {}).copy(),
    }


def _final_decision_to_dict(d: FinalDecision) -> dict[str, Any]:
    out: dict[str, Any] = {
        "action": d.action.value,
        "allowed": d.allowed,
        "reasons": list(d.reasons),
    }
    if d.mismatch:
        out["mismatch_flags"] = list(d.mismatch.flags)
        out["mismatch_reason_codes"] = list(d.mismatch.reason_codes)
    if d.params:
        out["params"] = dict(d.params)
    return out
