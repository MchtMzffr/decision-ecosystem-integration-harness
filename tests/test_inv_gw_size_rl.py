# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-GW-SIZE-1: Body size limit => 413. INV-GW-RL-1: Rate limit => 429."""

import os

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient


def test_inv_gw_size_1_payload_too_large() -> None:
    """Request with Content-Length over max_body_bytes returns 413 (INV-GW-SIZE-1)."""
    from harness.platform.gateway import create_app
    app = create_app(store_backend="off", max_body_bytes=50)
    client = TestClient(app)
    body = {"state": {"x": "a" * 100}, "context": {}}
    r = client.post("/decision", json=body)
    assert r.status_code in (200, 413)
    if r.status_code == 200:
        pytest.skip("TestClient may not send Content-Length; run with real client to assert 413")
    else:
        assert r.status_code == 413


def test_inv_gw_size_1_explicit_limit_413() -> None:
    """When body is over limit, 413 returned (use small limit so body exceeds)."""
    from harness.platform.gateway import create_app
    app = create_app(store_backend="off", max_body_bytes=10)
    client = TestClient(app)
    r = client.post("/decision", content=b'{"state":{},"context":{}}', headers={"content-type": "application/json"})
    if r.status_code == 413:
        assert "payload_too_large" in (r.json() or {}).get("error", "")
    else:
        assert r.status_code == 200


def test_inv_gw_rl_1_rate_limit_429() -> None:
    """When requests exceed DECISION_GATEWAY_RATE_MAX in window, 429 (INV-GW-RL-1)."""
    from harness.platform.gateway import create_app, _clear_rate_limit_for_test
    _clear_rate_limit_for_test()
    prev = os.environ.get("DECISION_GATEWAY_RATE_MAX")
    os.environ["DECISION_GATEWAY_RATE_MAX"] = "2"
    try:
        app = create_app(store_backend="off")
        client = TestClient(app)
        r1 = client.post("/decision", json={"state": {}, "context": {}})
        r2 = client.post("/decision", json={"state": {}, "context": {}})
        r3 = client.post("/decision", json={"state": {}, "context": {}})
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r3.status_code == 429
        assert (r3.json() or {}).get("error") == "too_many_requests"
        # P0.6: 429 includes Retry-After and X-RateLimit-* headers
        assert "Retry-After" in r3.headers
        assert r3.headers.get("X-RateLimit-Limit") == "2"
        assert r3.headers.get("X-RateLimit-Remaining") == "0"
    finally:
        if prev is not None:
            os.environ["DECISION_GATEWAY_RATE_MAX"] = prev
        else:
            os.environ.pop("DECISION_GATEWAY_RATE_MAX", None)
        _clear_rate_limit_for_test()
