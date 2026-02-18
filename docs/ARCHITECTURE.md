<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Integration Harness Architecture

## Role

The harness is the **integration layer** that wires the five cores into a single E2E pipeline. It is not a core; it depends on decision-schema (required) and optionally on mdm-engine, ops-health-core, dmc-core, evaluation-calibration-core.

## Data flow (single step)

```
state, context, now_ms
    → [MDM] propose(features) → Proposal
    → [Ops] update_kill_switch(state, policy, now_ms) → OpsSignal
    → context += ops_deny_actions, ops_state, ops_cooldown_until_ms
    → [DMC] modulate(proposal, GuardPolicy(), context) → (FinalDecision, MismatchInfo)
    → [Harness] build PacketV2 (input, external, mdm, final_action, latency_ms, schema_version)
    → [Eval-Cal] build_report([packet], expected_schema_minor=2) → Report
```

## Context registry (SSOT)

Context keys follow **decision-schema** PARAMETER_INDEX:

- `now_ms`, `run_id`, `last_event_ts_ms`
- `ops_deny_actions`, `ops_state`, `ops_cooldown_until_ms`
- `errors_in_window`, `steps_in_window`, `rate_limit_events`, `recent_failures`, `cooldown_until_ms`
- `fail_closed` (set by harness when exception path is taken)

## Invariants (harness-level)

- **H1**: Schema minor=2 compat (decision-schema 0.2.x)
- **H2**: Kill-switch dominance: ops_deny_actions=True ⇒ FinalDecision.allowed=False, action=HOLD
- **H3**: PacketV2 required fields present and non-empty
- **H4**: Fail-closed propagation: exception in any core ⇒ safe decision + context.fail_closed=True where applicable

## Optional cores

If a core is not installed, the harness still runs with fallbacks (e.g. no-MDM ⇒ HOLD proposal; no-DMC ⇒ pass-through FinalDecision; no eval-cal ⇒ report=None). Tests that require full stack should depend on optional `full` extras or skip when imports fail.
