# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Agent tool use. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps tool call request (tool_name, args) -> state/context; FinalDecision -> allow/deny + reason codes.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainAgentToolUseAdapter(BaseAdapter):
    """Example domain adapter: agent tool use (allow/deny). Not for production use."""

    def to_state_context(self, domain_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: tool_name, args -> state; optional caller_id -> context."""
        state = {
            "tool_name": domain_input.get("tool_name", ""),
            "args": domain_input.get("args", {}),
        }
        context: dict[str, Any] = {}
        if "caller_id" in domain_input:
            context["caller_id"] = domain_input["caller_id"]
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> allow, reason_codes."""
        return {
            "allow": final_decision.allowed,
            "reason_codes": list(final_decision.reasons),
        }
