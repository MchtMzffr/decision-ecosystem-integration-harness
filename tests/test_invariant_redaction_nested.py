# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT: Nested redaction — secret keys redacted at any depth (dict/list)."""

import pytest

from harness.redaction import REDACT_KEYS, redact_dict


def test_nested_dict_secret_redacted() -> None:
    """Nested dict with password/key must be redacted at every level."""
    data = {"user": {"name": "a", "password": "secret123"}, "api_key": "key"}
    out = redact_dict(data)
    assert out["user"]["name"] == "a"
    assert out["user"]["password"] == "[REDACTED]"
    assert out["api_key"] == "[REDACTED]"


def test_list_of_dicts_secret_redacted() -> None:
    """List of dicts: any secret key inside must be redacted."""
    data = {"items": [{"id": 1, "token": "t1"}, {"id": 2, "secret": "s2"}]}
    out = redact_dict(data)
    assert out["items"][0]["id"] == 1
    assert out["items"][0]["token"] == "[REDACTED]"
    assert out["items"][1]["id"] == 2
    assert out["items"][1]["secret"] == "[REDACTED]"


def test_deeply_nested_secret_redacted() -> None:
    """Deep nesting: inner dict with authorization must be redacted."""
    data = {"a": {"b": {"c": {"authorization": "Bearer xyz"}}}}
    out = redact_dict(data)
    assert out["a"]["b"]["c"]["authorization"] == "[REDACTED]"


def test_custom_keys_to_redact() -> None:
    """Custom keys_to_redact is applied in nested structures."""
    data = {"nested": {"custom_secret": "v"}}
    out = redact_dict(data, keys_to_redact=frozenset({"custom_secret"}))
    assert out["nested"]["custom_secret"] == "[REDACTED]"


def test_non_secret_preserved() -> None:
    """Non-sensitive keys and values are preserved."""
    data = {"signal_0": 1, "state_scalar_a": 0.5, "nested": {"public": "ok"}}
    out = redact_dict(data)
    assert out["signal_0"] == 1
    assert out["state_scalar_a"] == 0.5
    assert out["nested"]["public"] == "ok"
