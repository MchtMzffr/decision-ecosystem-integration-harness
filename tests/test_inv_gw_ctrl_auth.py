# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-GW-CTRL-LOCK-1: Control default disabled. INV-GW-AUTH-1: When enabled, token required."""

import os

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient


def test_inv_gw_ctrl_lock_1_default_disabled() -> None:
    """Without DECISION_GATEWAY_ENABLE_CONTROL, GET/POST /control return 403 (INV-GW-CTRL-LOCK-1)."""
    env_control = os.environ.pop("DECISION_GATEWAY_ENABLE_CONTROL", None)
    env_token = os.environ.pop("DECISION_CONTROL_TOKEN", None)
    try:
        from harness.platform.gateway import create_app
        app = create_app(store_backend="off", enable_control_endpoints=False)
        client = TestClient(app)
        r_get = client.get("/control")
        r_post = client.post("/control", json={"ops_state": "GREEN"})
        assert r_get.status_code == 403
        assert r_post.status_code == 403
    finally:
        if env_control is not None:
            os.environ["DECISION_GATEWAY_ENABLE_CONTROL"] = env_control
        if env_token is not None:
            os.environ["DECISION_CONTROL_TOKEN"] = env_token


def test_inv_gw_auth_1_token_required() -> None:
    """When control enabled, no token => 401; valid token => 200 (INV-GW-AUTH-1)."""
    env_control = os.environ.pop("DECISION_GATEWAY_ENABLE_CONTROL", None)
    env_token = os.environ.pop("DECISION_CONTROL_TOKEN", None)
    try:
        os.environ["DECISION_CONTROL_TOKEN"] = "secret123"
        from harness.platform.gateway import create_app
        app = create_app(store_backend="off", enable_control_endpoints=True)
        client = TestClient(app)
        r_no_token = client.get("/control")
        assert r_no_token.status_code == 401
        r_with_token = client.get("/control", headers={"X-Decision-Control-Token": "secret123"})
        assert r_with_token.status_code == 200
        r_post = client.post("/control", headers={"X-Decision-Control-Token": "secret123"}, json={"ops_state": "GREEN"})
        assert r_post.status_code == 200
    finally:
        if env_control is not None:
            os.environ["DECISION_GATEWAY_ENABLE_CONTROL"] = env_control
        elif "DECISION_GATEWAY_ENABLE_CONTROL" in os.environ:
            del os.environ["DECISION_GATEWAY_ENABLE_CONTROL"]
        if env_token is not None:
            os.environ["DECISION_CONTROL_TOKEN"] = env_token
        elif "DECISION_CONTROL_TOKEN" in os.environ:
            del os.environ["DECISION_CONTROL_TOKEN"]
