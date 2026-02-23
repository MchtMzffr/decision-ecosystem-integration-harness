# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Lending. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps lending-style input (income, debt, amount) -> state/context; FinalDecision -> approve/deny/limit.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainLendingAdapter(BaseAdapter):
    """Example domain adapter: lending (approve/deny/limit). Not for production use."""

    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: income, debt, amount_requested -> state; tenant/limits -> context."""
        state = {
            "income": domain_input.get("income", 0),
            "debt": domain_input.get("debt", 0),
            "amount_requested": domain_input.get("amount_requested", 0),
        }
        context = {}
        if "tenant" in domain_input:
            context["run_id"] = domain_input.get("run_id", "run-0")
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> result (approve|deny), limit, reasons."""
        return {
            "result": "approve"
            if final_decision.allowed and final_decision.action.value == "ACT"
            else "deny",
            "reasons": list(final_decision.reasons),
        }
