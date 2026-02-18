"""INVARIANT H2: Kill-switch dominance.
ops_deny_actions=True => FinalDecision deny + HOLD.
"""

import pytest
from decision_schema.types import Action, Proposal

pytestmark = pytest.mark.fullstack


def test_kill_switch_dominance_via_dmc() -> None:
    """When context has ops_deny_actions=True, DMC must return allowed=False, action=HOLD."""
    from dmc_core.dmc.modulator import modulate
    from dmc_core.dmc.policy import GuardPolicy

    proposal = Proposal(action=Action.ACT, confidence=0.9, reasons=["test"])

    context = {
        "now_ms": 1700000000000,
        "ops_deny_actions": True,
        "ops_state": "RED",
        "ops_cooldown_until_ms": None,
    }

    policy = GuardPolicy()
    final_decision, mismatch = modulate(proposal, policy, context)

    assert final_decision.allowed is False
    assert final_decision.action == Action.HOLD

    # mismatch surface is allowed to evolve; only require evidence of dominance routing.
    assert (
        ("ops_deny_actions" in (mismatch.reason_codes or []))
        or ("ops_health" in (mismatch.flags or []))
    )
