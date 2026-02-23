# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Store: persist PacketV2, Report, optional Explanation.
INV-STORE-SEC-1: Never write when harness.redaction_applied != True (fail-closed).
INV-STORE-NO-PII-1: Refuse write if payload hits secret/PII patterns.
INV-STORE-PATH-1: Default disallow absolute path; only allow under cwd or with allow_absolute_path=True.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from decision_schema.packet_v2 import PacketV2

# Minimal secret/PII patterns (INV-STORE-NO-PII-1). No logging of matched content.
_SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}", re.I),
    re.compile(r"password\s*=\s*['\"]?\S+", re.I),
    re.compile(r"api[_-]?key\s*=\s*['\"]?\S+", re.I),
    re.compile(r"bearer\s+[a-zA-Z0-9_.-]{20,}", re.I),
]


def _redaction_ok(packet: PacketV2) -> bool:
    """INV-STORE-SEC-1: Only write when redaction was applied by harness."""
    return packet.external.get("harness.redaction_applied") is True


def _has_secret_pattern(obj: Any) -> bool:
    """INV-STORE-NO-PII-1: True if any string in obj matches secret patterns."""
    if isinstance(obj, str):
        return any(p.search(obj) for p in _SECRET_PATTERNS)
    if isinstance(obj, dict):
        return any(_has_secret_pattern(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_secret_pattern(v) for v in obj)
    return False


def save(
    packet: PacketV2,
    report: Any | None = None,
    explanation: Any | None = None,
    backend: str = "memory",
    path: str | Path | None = None,
    allow_absolute_path: bool = False,
    _memory_buffer: list[dict[str, Any]] | None = None,
) -> None:
    """
    Persist one step. backend=off or empty => no-op.
    INV-STORE-SEC-1: If packet.external has no harness.redaction_applied=True, do not write (fail-closed).
    INV-STORE-NO-PII-1: If payload matches secret/PII patterns, do not write.
    INV-STORE-PATH-1: If backend=file and path is absolute and allow_absolute_path is False, do not write (raise ValueError).
    """
    if backend == "off" or not backend:
        return
    if not _redaction_ok(packet):
        return
    payload = {"packet": packet.to_dict()}
    if _has_secret_pattern(payload):
        return
    if backend == "memory":
        buf = _memory_buffer if _memory_buffer is not None else _default_memory_buffer
        entry: dict[str, Any] = dict(payload)
        if report is not None and hasattr(report, "suite_name"):
            entry["report_suite"] = getattr(report, "suite_name", None)
        if report is not None and hasattr(report, "contract_matrix_check"):
            entry["contract_ok"] = (report.contract_matrix_check or {}).get(
                "compatible"
            ) is True
        if explanation is not None and hasattr(explanation, "to_dict"):
            entry["explanation"] = explanation.to_dict()
        buf.append(entry)
        return
    if backend == "file":
        if path is None:
            path = os.environ.get("DECISION_STORE_PATH", "decision_audit.jsonl")
        p = Path(path)
        if p.is_absolute() and not allow_absolute_path:
            raise ValueError(
                "INV-STORE-PATH-1: absolute store path not allowed by default; set allow_absolute_path=True to override"
            )
        p = p.resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        entry = dict(payload)
        if report is not None and hasattr(report, "suite_name"):
            entry["report_suite"] = getattr(report, "suite_name", None)
        if explanation is not None and hasattr(explanation, "to_dict"):
            entry["explanation"] = explanation.to_dict()
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()
            if hasattr(os, "fsync"):
                os.fsync(f.fileno())
        return
    raise ValueError(f"Unknown store backend: {backend}")


_default_memory_buffer: list[dict[str, Any]] = []


def get_memory_buffer() -> list[dict[str, Any]]:
    return _default_memory_buffer


def clear_memory_buffer() -> None:
    _default_memory_buffer.clear()
