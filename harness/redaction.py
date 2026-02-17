"""Redaction helpers for input/external dicts before PacketV2 (no secrets in trace)."""

from __future__ import annotations

from typing import Any

# Keys that must be redacted in integration traces (PARAMETER_INDEX / security)
REDACT_KEYS = frozenset({"password", "secret", "api_key", "token", "authorization"})


def redact_dict(d: dict[str, Any], keys_to_redact: frozenset[str] | None = None) -> dict[str, Any]:
    """
    Return a copy of the dict with sensitive keys redacted (value replaced by "[REDACTED]").
    Recurses one level into nested dicts only (shallow nested redaction).
    """
    keys = keys_to_redact or REDACT_KEYS
    out: dict[str, Any] = {}
    for k, v in d.items():
        key_lower = k.lower()
        if any(red in key_lower for red in keys):
            out[k] = "[REDACTED]"
        elif isinstance(v, dict) and not isinstance(v, type(out)):
            out[k] = redact_dict(dict(v), keys)
        else:
            out[k] = v
    return out
