# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Scheduling. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps slot request (date, duration, resource_id) -> state/context; FinalDecision -> slot_ok, suggested_slots.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainSchedulingAdapter(BaseAdapter):
    """Example domain adapter: scheduling (slot availability). Not for production use."""

    def to_state_context(self, domain_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: date, duration_min, resource_id -> state; context empty or tenant."""
        state = {
            "date": domain_input.get("date", ""),
            "duration_min": domain_input.get("duration_min", 30),
            "resource_id": domain_input.get("resource_id", ""),
        }
        context = {}
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> slot_ok, suggested_slots (empty for deny)."""
        return {
            "slot_ok": final_decision.allowed,
            "suggested_slots": [] if not final_decision.allowed else [],
            "reasons": list(final_decision.reasons),
        }
