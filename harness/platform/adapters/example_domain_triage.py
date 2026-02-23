# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Triage. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps ticket/case -> state/context; FinalDecision -> risk level and human review recommendation.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainTriageAdapter(BaseAdapter):
    """Example domain adapter: triage (priority, escalate, human review). Not for production use."""

    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: ticket_id, summary, category -> state; context optional."""
        state = {
            "ticket_id": domain_input.get("ticket_id", ""),
            "summary": domain_input.get("summary", ""),
            "category": domain_input.get("category", ""),
        }
        context: dict[str, Any] = {}
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> risk_level, escalate, human_review, reasons."""
        return {
            "risk_level": "high" if not final_decision.allowed else "low",
            "escalate": not final_decision.allowed,
            "human_review": not final_decision.allowed,
            "reasons": list(final_decision.reasons),
        }
