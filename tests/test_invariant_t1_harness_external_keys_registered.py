"""INVARIANT T1: Harness external keys are registered in SSOT registry."""

from __future__ import annotations

from decision_schema.trace_registry import EXTERNAL_KEY_REGISTRY, validate_external_dict


def test_inv_t1_harness_fail_closed_key_is_registered() -> None:
    """harness.fail_closed must be in SSOT registry."""
    assert "harness.fail_closed" in EXTERNAL_KEY_REGISTRY


def test_inv_t1_harness_fail_closed_key_validates_in_strict_mode() -> None:
    """harness.fail_closed validates in strict mode (registered)."""
    errors = validate_external_dict(
        {"harness.fail_closed": True},
        require_registry_for_prefixes={"harness"},
    )
    assert errors == []
