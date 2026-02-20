# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT T1 / INV-TRACE-REG-1: Harness external keys are registered in SSOT registry."""

from __future__ import annotations

from decision_schema.trace_registry import EXTERNAL_KEY_REGISTRY, validate_external_dict

# Prefixes that the integration stack (harness + cores) may emit; all must be registered in strict mode.
STRICT_PREFIXES = frozenset({"harness", "exec"})


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


def test_inv_trace_reg_1_all_registry_keys_pass_strict_validation() -> None:
    """INV-TRACE-REG-1: Every key in EXTERNAL_KEY_REGISTRY validates in strict mode for its prefix."""
    for key in EXTERNAL_KEY_REGISTRY:
        prefix = key.split(".", 1)[0]
        if prefix not in STRICT_PREFIXES:
            continue
        errors = validate_external_dict(
            {key: None},
            require_registry_for_prefixes=STRICT_PREFIXES,
        )
        assert errors == [], (
            f"Registered key {key!r} must validate in strict mode: {errors}"
        )


def test_inv_trace_reg_1_unregistered_trace_key_fails_strict() -> None:
    """INV-TRACE-REG-1: Unregistered trace key under strict prefix fails validation."""
    errors = validate_external_dict(
        {"harness.unregistered_future_key": True},
        require_registry_for_prefixes=STRICT_PREFIXES,
    )
    assert any("unregistered_key" in e for e in errors)
