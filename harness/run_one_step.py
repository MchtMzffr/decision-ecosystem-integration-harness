"""
Single-step pipeline: propose → ops signal → modulate → PacketV2 → report.

Contract: state (dict), context (dict), now_ms (int) → (FinalDecision, PacketV2, Report).
Context keys follow decision-schema PARAMETER_INDEX (now_ms, ops_deny_actions, etc.).
"""

from __future__ import annotations

import time
from typing import Any

from decision_schema.types import Action, FinalDecision, MismatchInfo, Proposal

from harness.packet_builder import build_packet_v2


def run_one_step(
    state: dict[str, Any],
    context: dict[str, Any],
    now_ms: int,
    run_id: str = "run-0",
    step: int = 0,
) -> tuple[FinalDecision, Any, Any]:
    """
    Run one E2E step: MDM propose → ops update_kill_switch → context merge → DMC modulate → PacketV2 → build_report.

    Returns:
        (final_decision, packet_v2, report).
        If a core is not installed, that step is skipped or a minimal stub is used (see impl).
    """
    t0 = time.perf_counter()
    context = dict(context)
    context["now_ms"] = now_ms
    context.setdefault("run_id", run_id)

    # 1) Propose (mdm-engine)
    proposal = _propose(state, context)

    # 2) Ops kill switch
    ops_signal = _update_ops(context, now_ms)
    context["ops_deny_actions"] = ops_signal.get("ops_deny_actions", False)
    context["ops_state"] = ops_signal.get("ops_state", "GREEN")
    context["ops_cooldown_until_ms"] = ops_signal.get("ops_cooldown_until_ms")

    # 3) Modulate (DMC)
    final_decision, mismatch = _modulate(proposal, context)

    # 4) PacketV2
    latency_ms = int((time.perf_counter() - t0) * 1000)
    mismatch_dict = None
    if mismatch and (mismatch.flags or mismatch.reason_codes):
        mismatch_dict = {"flags": list(mismatch.flags), "reason_codes": list(mismatch.reason_codes)}
    packet = build_packet_v2(
        run_id=run_id,
        step=step,
        input_snapshot=state,
        external_snapshot=context,
        proposal=proposal,
        final_decision=final_decision,
        latency_ms=latency_ms,
        mismatch=mismatch_dict,
    )

    # 5) Report (eval-calibration)
    report = _build_report([packet])

    return final_decision, packet, report


def _propose(state: dict[str, Any], context: dict[str, Any]) -> Proposal:
    """Proposal from MDM; state used as features for minimal harness."""
    try:
        from mdm_engine.mdm.decision_engine import DecisionEngine
        engine = DecisionEngine(confidence_threshold=0.5)
        features = _state_to_features(state, context)
        return engine.propose(features)
    except ImportError:
        return Proposal(action=Action.HOLD, confidence=0.0, reasons=["harness_no_mdm"])


def _state_to_features(state: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Domain-agnostic passthrough: state keys are already generic (signal_0/1, state_scalar_a/b)."""
    features = dict(state)
    if "now_ms" in context:
        features["now_ms"] = context["now_ms"]
    return features


def _update_ops(context: dict[str, Any], now_ms: int) -> dict[str, Any]:
    """Ops kill switch signal; merge into context-style dict."""
    try:
        from ops_health_core.kill_switch import update_kill_switch
        from ops_health_core.model import OpsPolicy, OpsState
        policy = OpsPolicy()
        ops_state = OpsState(
            error_timestamps=context.get("error_timestamps", []),
            rate_limit_timestamps=context.get("rate_limit_timestamps", []),
            cooldown_until_ms=context.get("ops_cooldown_until_ms"),
        )
        signal = update_kill_switch(ops_state, policy, now_ms)
        return signal.to_context()
    except ImportError:
        return {"ops_deny_actions": False, "ops_state": "GREEN", "ops_cooldown_until_ms": None}


def _modulate(proposal: Proposal, context: dict[str, Any]) -> tuple[FinalDecision, Any]:
    """DMC modulate; return (FinalDecision, MismatchInfo)."""
    try:
        from dmc_core.dmc.modulator import modulate
        from dmc_core.dmc.policy import GuardPolicy
        policy = GuardPolicy()
        return modulate(proposal, policy, context)
    except ImportError:
        return (
            FinalDecision(action=proposal.action, allowed=True, reasons=proposal.reasons),
            MismatchInfo(flags=[], reason_codes=[]),
        )


def _build_report(packets: list) -> Any:
    """Build report from packets (eval-calibration-core)."""
    try:
        from eval_calibration_core.report.builder import build_report
        return build_report(packets, suite_name="harness", expected_schema_minor=2)
    except ImportError:
        return None
