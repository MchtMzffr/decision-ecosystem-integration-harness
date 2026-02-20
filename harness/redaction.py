# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Redaction helpers for input/external dicts before PacketV2 (no secrets in trace)."""

from __future__ import annotations

from typing import Any

# Keys that must be redacted in integration traces (PARAMETER_INDEX / security)
REDACT_KEYS = frozenset({"password", "secret", "api_key", "token", "authorization"})


def _normalize_key(key: str) -> str:
    """Normalize for comparison: lower, no dashes/underscores."""
    return key.lower().replace("-", "").replace("_", "")


def _key_matches_redact(key: str, keys_to_redact: frozenset[str]) -> bool:
    """True if key (case-insensitive, normalized) matches any redact key (substring or exact)."""
    key_norm = _normalize_key(key)
    for red in keys_to_redact:
        if _normalize_key(red) in key_norm:
            return True
    return False


def redact_dict(
    d: dict[str, Any], keys_to_redact: frozenset[str] | None = None
) -> dict[str, Any]:
    """
    Return a copy of the dict with sensitive keys redacted (value replaced by "[REDACTED]").
    Recurses into nested dicts and into list elements that are dicts (deterministic, no leak).
    """
    keys = keys_to_redact or REDACT_KEYS
    out: dict[str, Any] = {}
    for k, v in d.items():
        if _key_matches_redact(k, keys):
            out[k] = "[REDACTED]"
        elif isinstance(v, dict):
            out[k] = redact_dict(dict(v), keys)
        elif isinstance(v, list):
            out[k] = [redact_dict(x, keys) if isinstance(x, dict) else x for x in v]
        else:
            out[k] = v
    return out
