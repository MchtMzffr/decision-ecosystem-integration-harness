# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Catalog: policy/context overrides from env. Used by gateway or caller."""

from __future__ import annotations

import os
from typing import Any


def get_context_overrides(tenant_id: str | None = None) -> dict[str, Any]:
    """Return context overrides from env (PARAMETER_INDEX keys)."""
    overrides: dict[str, Any] = {}
    v = os.environ.get("DECISION_OPS_DENY_ACTIONS", "").strip().lower()
    if v in ("1", "true", "yes"):
        overrides["ops_deny_actions"] = True
    if os.environ.get("DECISION_OPS_STATE"):
        overrides["ops_state"] = os.environ.get("DECISION_OPS_STATE", "GREEN").strip()
    if tenant_id and os.environ.get(f"DECISION_TENANT_{tenant_id}_OPS_STATE"):
        overrides["ops_state"] = os.environ.get(f"DECISION_TENANT_{tenant_id}_OPS_STATE", "GREEN").strip()
    return overrides


def get_policy_defaults() -> dict[str, Any]:
    """Return policy defaults from env (e.g. staleness_ms)."""
    defaults: dict[str, Any] = {}
    s = os.environ.get("DECISION_STALENESS_MS")
    if s is not None:
        try:
            defaults["staleness_ms"] = int(s)
        except ValueError:
            pass
    return defaults


def merge_context(base: dict[str, Any], overrides: dict[str, Any] | None) -> dict[str, Any]:
    """Merge overrides into base context."""
    out = dict(base)
    if overrides:
        out.update(overrides)
    return out
