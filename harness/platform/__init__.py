# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Platform layer: Gateway, Catalog, Control, Store, Adapters.

INV-PLAT-ISOLATION-1: Platform modules do not change pipeline semantics; they only orchestrate.
Pipeline SSOT remains harness.run_one_step (unchanged).
"""

from harness.platform.catalog import (
    get_context_overrides,
    get_policy_defaults,
    merge_context,
)
from harness.platform.control import (
    clear_ops_override,
    get_ops_state,
    set_green,
    set_ops_state,
    set_red,
)
from harness.platform.store import (
    clear_memory_buffer,
    get_memory_buffer,
    save as store_save,
)

__all__ = [
    "get_context_overrides",
    "get_policy_defaults",
    "merge_context",
    "get_ops_state",
    "set_ops_state",
    "set_red",
    "set_green",
    "clear_ops_override",
    "store_save",
    "get_memory_buffer",
    "clear_memory_buffer",
]
