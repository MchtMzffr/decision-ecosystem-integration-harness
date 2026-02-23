# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Example domain: Trading. For illustration only (INV-ADAPTER-DOMAIN-LEAK-1).
Maps trading-style input (price, position, pnl) -> state/context; FinalDecision -> buy/sell/hold.
"""

from __future__ import annotations

from typing import Any

from decision_schema.types import FinalDecision

from harness.platform.adapters.base import BaseAdapter


class ExampleDomainTradingAdapter(BaseAdapter):
    """Example domain adapter: trading (buy/sell/hold). Not for production use."""

    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Example: price, position, daily_pnl -> state; context optional."""
        state = {
            "price": domain_input.get("price", 0.0),
            "position": domain_input.get("position", 0),
            "daily_pnl": domain_input.get("daily_pnl", 0.0),
        }
        context = {}
        return (state, context)

    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Example: FinalDecision -> action (buy|sell|hold), reasons."""
        return {
            "action": "hold"
            if not final_decision.allowed
            else final_decision.action.value.lower(),
            "reasons": list(final_decision.reasons),
        }
