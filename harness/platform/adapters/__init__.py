# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Adapters: domain input -> (state, context); (FinalDecision, Report) -> domain output.
INV-ADAPTER-DOMAIN-LEAK-1: Adapter names and docs carry "Example domain" label; no production domain in public API.
"""

from harness.platform.adapters.base import BaseAdapter
from harness.platform.adapters.example_domain_lending import ExampleDomainLendingAdapter
from harness.platform.adapters.example_domain_scheduling import ExampleDomainSchedulingAdapter
from harness.platform.adapters.example_domain_trading import ExampleDomainTradingAdapter

_REGISTRY: dict[str, type[BaseAdapter]] = {
    "example_domain_lending": ExampleDomainLendingAdapter,
    "example_domain_scheduling": ExampleDomainSchedulingAdapter,
    "example_domain_trading": ExampleDomainTradingAdapter,
}


def get_adapter(name: str) -> BaseAdapter:
    """Return adapter instance by name. Raises KeyError if unknown."""
    cls = _REGISTRY[name]
    return cls()


__all__ = [
    "BaseAdapter",
    "get_adapter",
    "ExampleDomainLendingAdapter",
    "ExampleDomainSchedulingAdapter",
    "ExampleDomainTradingAdapter",
]
