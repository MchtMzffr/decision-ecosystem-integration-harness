<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Integration Guide

## Installing the harness

```bash
pip install -e .
# Full E2E (all cores):
pip install -e ".[full]"
```

## Running one step

```python
from harness import run_one_step

state = {"signal_0": 0.5, "signal_1": 0.1, "state_scalar_a": 50.0, "state_scalar_b": 10.0}
context = {"now_ms": 1700000000000}
now_ms = 1700000000000

final_decision, packet, report = run_one_step(state, context, now_ms, run_id="run-1", step=0)
# final_decision: FinalDecision
# packet: PacketV2
# report: Report or None if eval-calibration-core not installed
```

## Context keys (from PARAMETER_INDEX)

Set these in `context` for DMC guards and trace:

- `now_ms`, `last_event_ts_ms`, `run_id`
- Ops: set by harness from `update_kill_switch` → `ops_deny_actions`, `ops_state`, `ops_cooldown_until_ms`
- Optional: `errors_in_window`, `steps_in_window`, `rate_limit_events`, `recent_failures`, `cooldown_until_ms`

## Invariant tests

- `tests/test_invariant_h1_schema_minor_2.py`: Schema 0.2.x compat
- `tests/test_invariant_h2_kill_switch_dominance.py`: ops_deny_actions ⇒ deny + HOLD
- `tests/test_invariant_h3_packet_trace_completeness.py`: PacketV2 required fields
- `tests/test_end_to_end_smoke.py`: Single-step run (with or without full cores)

## Redaction

`harness.redaction.redact_dict(d)` redacts sensitive keys (password, secret, api_key, etc.) before putting input/external into PacketV2. Use it if you pass raw state/context that may contain secrets.
