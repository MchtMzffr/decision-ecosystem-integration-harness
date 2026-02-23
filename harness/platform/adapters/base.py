# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Base adapter: domain -> (state, context); (FinalDecision, Report) -> domain output. Example domain only."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from decision_schema.types import FinalDecision


class BaseAdapter(ABC):
    """Domain-agnostic adapter. Implementations are Example domain only (INV-ADAPTER-DOMAIN-LEAK-1)."""

    @abstractmethod
    def to_state_context(
        self, domain_input: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Map domain request to (state, context) for run_one_step."""
        ...

    @abstractmethod
    def to_domain_output(
        self,
        final_decision: FinalDecision,
        report: Any | None,
        packet: Any,
    ) -> dict[str, Any]:
        """Map pipeline output to domain response dict."""
        ...
