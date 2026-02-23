# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-GW-FAILCLOSED-1: Gateway exception => allowed=false and packet trace marker."""

import sys

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient


def test_gateway_exception_returns_fail_closed() -> None:
    """When run_one_step raises, gateway returns 500 with final_decision.allowed=false (INV-GW-FAILCLOSED-1)."""
    from harness.platform.gateway import create_app

    def raise_exc(*args: object, **kwargs: object) -> None:
        raise RuntimeError("injected")

    run_mod = sys.modules["harness.run_one_step"]
    original = getattr(run_mod, "run_one_step")
    run_mod.run_one_step = raise_exc  # type: ignore[assignment]
    try:
        app = create_app(
            store_backend="off", use_catalog=False, use_control_in_context=False
        )
        client = TestClient(app)
        r = client.post("/decision", json={"state": {}, "context": {}})
    finally:
        run_mod.run_one_step = original
    assert r.status_code == 500
    data = r.json()
    assert data.get("final_decision", {}).get("allowed") is False
    assert "gateway_fail_closed" in (
        data.get("final_decision", {}).get("reasons") or []
    )
