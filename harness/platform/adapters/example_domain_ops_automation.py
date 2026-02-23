# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Ops automation. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps ops request (operation, target, params) -> state/context; FinalDecision -> allow/deny + reason codes.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainOpsAutomationAdapter(BaseAdapter):
    """Example domain adapter: ops automation (allow/deny). Not for production use."""

    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: operation, target, params -> state; guards config -> context."""
        state = {
            "operation": domain_input.get("operation", ""),
            "target": domain_input.get("target", ""),
            "params": domain_input.get("params", {}),
        }
        context: dict[str, Any] = {}
        if "run_id" in domain_input:
            context["run_id"] = domain_input["run_id"]
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> allowed, reason_codes."""
        return {
            "allowed": final_decision.allowed,
            "reason_codes": list(final_decision.reasons),
        }
