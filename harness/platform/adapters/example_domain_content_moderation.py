# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Content moderation. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps text/comment -> state/context; FinalDecision -> risk level and decision (allow/flag/block).
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainContentModerationAdapter(BaseAdapter):
    """Example domain adapter: content moderation (allow/flag/block). Not for production use."""

    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: text, comment_id -> state; optional metadata -> context."""
        state = {
            "text": domain_input.get("text", ""),
            "comment_id": domain_input.get("comment_id", ""),
        }
        context: dict[str, Any] = {}
        if "metadata" in domain_input:
            context["metadata"] = domain_input["metadata"]
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> decision (allow|flag|block), risk, reason_codes."""
        decision = "allow" if final_decision.allowed else "block"
        if final_decision.allowed and final_decision.action.value != "ACT":
            decision = "flag"
        return {
            "decision": decision,
            "risk": "low" if final_decision.allowed else "high",
            "reason_codes": list(final_decision.reasons),
        }
