# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Gateway: HTTP API for the decision pipeline. Orchestration only; pipeline SSOT is run_one_step (INV-PLAT-ISOLATION-1).
POST /decide (and /decision legacy), GET/POST /control. INV-GW-FAILCLOSED-1: exception => allowed=false + packet trace.
INV-DEPS-OPTIONAL-1: server deps only with [gateway] or [server] extra.
"""

from __future__ import annotations

import os
import time
from typing import Any

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except ImportError as e:
    FastAPI = None  # type: ignore
    _gateway_import_error = e


def _control_enabled() -> bool:
    """INV-GW-CTRL-LOCK-1: Control endpoints disabled unless DECISION_GATEWAY_ENABLE_CONTROL=1."""
    return os.environ.get("DECISION_GATEWAY_ENABLE_CONTROL", "0").strip().lower() in ("1", "true", "yes")


def _control_token_ok(request: Request) -> bool:
    """INV-GW-AUTH-1: When control enabled, token required (X-Decision-Control-Token or Authorization: Bearer)."""
    expected = os.environ.get("DECISION_CONTROL_TOKEN", "").strip()
    if not expected:
        return False
    token = request.headers.get("X-Decision-Control-Token", "").strip()
    if not token and request.headers.get("Authorization", "").startswith("Bearer "):
        token = request.headers["Authorization"][7:].strip()
    return token == expected and bool(token)


def create_app(
    store_backend: str = "memory",
    store_path: str | None = None,
    use_catalog: bool = True,
    use_control_in_context: bool = True,
    enable_control_endpoints: bool | None = None,
) -> Any:
    """
    Create FastAPI app. Requires pip install .[gateway] (INV-DEPS-OPTIONAL-1).
    INV-GW-CTRL-LOCK-1: Control endpoints disabled by default (enable_control_endpoints or DECISION_GATEWAY_ENABLE_CONTROL).
    INV-GW-AUTH-1: When enabled, DECISION_CONTROL_TOKEN header required for GET/POST /control.
    """
    if FastAPI is None:
        raise ImportError(
            "Gateway requires FastAPI and uvicorn. Install with: pip install decision-ecosystem-integration-harness[gateway]"
        ) from _gateway_import_error

    from harness.platform.catalog import get_context_overrides, merge_context
    from harness.platform.control import get_ops_state, set_ops_state
    from harness.platform.store import save as store_save
    from harness.run_one_step import run_one_step

    control_enabled = enable_control_endpoints if enable_control_endpoints is not None else _control_enabled()
    app = FastAPI(title="Decision Ecosystem Gateway", version="0.1.0")

    def _run_and_respond(
        state: dict[str, Any],
        context: dict[str, Any],
        run_id: str,
        step: int,
        tenant_id: str | None,
        now_ms: int,
    ) -> tuple[dict[str, Any], int, Any, Any, Any]:
        """Run pipeline; return (body, status_code, final_decision, packet, report). INV-GW-FAILCLOSED-1 on exception."""
        if use_catalog:
            overrides = get_context_overrides(tenant_id)
            context = merge_context(context, overrides)
        if use_control_in_context:
            ops = get_ops_state()
            if ops:
                context = {**context, **ops}
        try:
            final_decision, packet, report = run_one_step(
                state=state,
                context=context,
                now_ms=now_ms,
                run_id=run_id,
                step=step,
            )
        except Exception as e:
            return (
                {
                    "error": "pipeline_error",
                    "detail": str(e),
                    "final_decision": {"action": "HOLD", "allowed": False, "reasons": ["gateway_fail_closed"]},
                    "packet": None,
                },
                500,
                None,
                None,
                None,
            )
        out: dict[str, Any] = {
            "final_decision": {
                "action": final_decision.action.value,
                "allowed": final_decision.allowed,
                "reasons": list(final_decision.reasons),
            },
            "packet": {
                "run_id": packet.run_id,
                "step": packet.step,
                "latency_ms": packet.latency_ms,
            },
        }
        if report is not None and hasattr(report, "suite_name"):
            out["report_suite"] = report.suite_name
        if store_backend and store_backend != "off":
            store_save(packet, report, backend=store_backend, path=store_path)
        return (out, 200, final_decision, packet, report)

    from harness.platform.adapters import get_adapter as _get_adapter

    @app.post("/decide")
    async def decide(request: Request) -> JSONResponse:
        """
        Domain-agnostic contract.
        Input: { "adapter": "example_domain_lending"|null, "input": {...}, "tenant": "...", "policy_id": "...", "idempotency_key": "..." }.
        If adapter is set, input is passed to adapter.to_state_context(); else input is used as state and context from body.
        Output: { "final_decision": {...}, "packet": {...}, "report_suite": ..., "domain_output": ... (if adapter) }.
        """
        try:
            body = await request.json()
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": "invalid_json", "detail": str(e)})
        adapter_name = body.get("adapter")
        raw_input = body.get("input", {})
        tenant = body.get("tenant")
        idempotency_key = body.get("idempotency_key")
        run_id = body.get("run_id", idempotency_key or "run-0")
        step = int(body.get("step", 0))
        now_ms = int(time.time() * 1000)
        if adapter_name:
            try:
                adapter = _get_adapter(adapter_name)
                state, context = adapter.to_state_context(raw_input)
            except (ImportError, KeyError) as e:
                return JSONResponse(status_code=400, content={"error": "adapter", "detail": str(e)})
        else:
            state = raw_input.get("state", raw_input)
            context = raw_input.get("context", {})
        out, status, fd, packet, report = _run_and_respond(state, context, run_id, step, tenant, now_ms)
        if status != 200:
            return JSONResponse(status_code=status, content=out)
        if adapter_name and fd is not None and packet is not None:
            adapter = _get_adapter(adapter_name)
            out["domain_output"] = adapter.to_domain_output(fd, report, packet)
        return JSONResponse(content=out)

    @app.post("/decision")
    async def decision(request: Request) -> JSONResponse:
        """Legacy: body { "state": {...}, "context": {...}, "run_id": "...", "step": 0, "tenant_id": "..." }."""
        try:
            body = await request.json()
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": "invalid_json", "detail": str(e)})
        state = body.get("state", {})
        context = body.get("context", {})
        run_id = body.get("run_id", "run-0")
        step = int(body.get("step", 0))
        tenant_id = body.get("tenant_id")
        now_ms = int(time.time() * 1000)
        out, status, _fd, _packet, _report = _run_and_respond(state, context, run_id, step, tenant_id, now_ms)
        return JSONResponse(status_code=status, content=out)

    @app.get("/control")
    async def control_get(request: Request) -> JSONResponse:
        if not control_enabled:
            return JSONResponse(status_code=403, content={"error": "control_disabled", "detail": "Set DECISION_GATEWAY_ENABLE_CONTROL=1 to enable"})
        if not _control_token_ok(request):
            return JSONResponse(status_code=401, content={"error": "unauthorized", "detail": "X-Decision-Control-Token or Authorization: Bearer required"})
        return JSONResponse(content=get_ops_state())

    @app.post("/control")
    async def control_post(request: Request) -> JSONResponse:
        if not control_enabled:
            return JSONResponse(status_code=403, content={"error": "control_disabled", "detail": "Set DECISION_GATEWAY_ENABLE_CONTROL=1 to enable"})
        if not _control_token_ok(request):
            return JSONResponse(status_code=401, content={"error": "unauthorized", "detail": "X-Decision-Control-Token or Authorization: Bearer required"})
        try:
            body = await request.json()
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        set_ops_state(
            ops_deny_actions=body.get("ops_deny_actions"),
            ops_state=body.get("ops_state"),
            ops_cooldown_until_ms=body.get("ops_cooldown_until_ms"),
        )
        return JSONResponse(content=get_ops_state())

    @app.get("/health")
    async def health() -> JSONResponse:
        return JSONResponse(content={"status": "ok"})

    return app


def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
    store_backend: str = "memory",
    store_path: str | None = None,
) -> None:
    """Run gateway with uvicorn. Requires [gateway] extra (INV-DEPS-OPTIONAL-1)."""
    try:
        import uvicorn
    except ImportError as e:
        raise ImportError(
            "serve() requires uvicorn. Install with: pip install decision-ecosystem-integration-harness[gateway]"
        ) from e
    app = create_app(store_backend=store_backend, store_path=store_path)
    uvicorn.run(app, host=host, port=port)
