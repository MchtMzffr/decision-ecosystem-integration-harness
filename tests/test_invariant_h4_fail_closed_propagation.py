# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT H4: Fail-closed propagation.
Exception in run_one_step => FinalDecision(allowed=False, action=HOLD) + packet.external["harness.fail_closed"].
"""

import sys
import pytest
from decision_schema.types import Action

pytestmark = pytest.mark.fullstack


def _run_one_step_module():
    """Module that defines run_one_step (for monkeypatching _propose/_modulate)."""
    import harness.run_one_step as _  # noqa: F401

    return sys.modules["harness.run_one_step"]


def test_fail_closed_on_exception_proposal(monkeypatch: pytest.MonkeyPatch) -> None:
    """When _propose raises, run_one_step returns deny + HOLD and packet with fail_closed."""
    from harness.run_one_step import run_one_step

    def raise_in_propose(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("injected")

    monkeypatch.setattr(_run_one_step_module(), "_propose", raise_in_propose)
    state = {"signal_0": 1}
    context = {"now_ms": 1700000000000}
    final_decision, packet, _report = run_one_step(
        state, context, context["now_ms"], run_id="r", step=0
    )

    assert final_decision.allowed is False
    assert final_decision.action == Action.HOLD
    assert "fail_closed_exception" in final_decision.reasons
    assert packet.external.get("harness.fail_closed") is True
    assert packet.final_action["action"] == Action.HOLD.value
    assert packet.final_action["allowed"] is False


def test_fail_closed_on_exception_modulate(monkeypatch: pytest.MonkeyPatch) -> None:
    """When _modulate raises, run_one_step returns deny + HOLD and packet with fail_closed."""
    from harness.run_one_step import run_one_step

    def raise_in_modulate(*_args: object, **_kwargs: object) -> None:
        raise ValueError("injected modulate")

    monkeypatch.setattr(_run_one_step_module(), "_modulate", raise_in_modulate)
    state = {"signal_0": 1}
    context = {"now_ms": 1700000000000}
    final_decision, packet, _report = run_one_step(
        state, context, context["now_ms"], run_id="r", step=0
    )

    assert final_decision.allowed is False
    assert final_decision.action == Action.HOLD
    assert packet.external.get("harness.fail_closed") is True
