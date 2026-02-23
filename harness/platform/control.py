# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Control: read/write ops state (kill-switch, cooldown) for the pipeline.
Gateway merges get_ops_state() into context; pipeline semantics unchanged (INV-PLAT-ISOLATION-1).
INV-CTRL-DOM-1: kill-switch ON => all decisions deny (ops-health dominance).
"""

from __future__ import annotations

from typing import Any

_ops_override: dict[str, Any] = {}


def get_ops_state() -> dict[str, Any]:
    """Return current ops override (ops_deny_actions, ops_state, ops_cooldown_until_ms)."""
    return dict(_ops_override)


def set_ops_state(
    ops_deny_actions: bool | None = None,
    ops_state: str | None = None,
    ops_cooldown_until_ms: int | None = None,
) -> None:
    """Set ops override. ops_state: GREEN | YELLOW | RED."""
    global _ops_override
    if ops_deny_actions is not None:
        _ops_override["ops_deny_actions"] = ops_deny_actions
    if ops_state is not None:
        _ops_override["ops_state"] = str(ops_state).upper()
    if ops_cooldown_until_ms is not None:
        _ops_override["ops_cooldown_until_ms"] = ops_cooldown_until_ms


def set_red() -> None:
    """Convenience: deny all actions (kill-switch RED)."""
    set_ops_state(ops_deny_actions=True, ops_state="RED")


def set_green() -> None:
    """Convenience: allow actions (GREEN)."""
    set_ops_state(ops_deny_actions=False, ops_state="GREEN")


def clear_ops_override() -> None:
    """Clear in-memory ops override (e.g. for tests)."""
    global _ops_override
    _ops_override.clear()
