<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Formulas (Harness)

Key formulas and checks used in the integration harness.

## Schema compatibility (H1)

- Gate: `decision_schema.compat.is_compatible(version, expected_major=0, min_minor=2, max_minor=2)`
- Expected: 0.2.x only (single minor pin).

## Kill-switch dominance (H2)

- Condition: `context["ops_deny_actions"] == True` (from ops-health-core OpsSignal).
- Expected: DMC ops_health_guard fails; FinalDecision.allowed == False, FinalDecision.action == Action.HOLD; mismatch reason code reflects ops.

## PacketV2 completeness (H3)

Required fields (PARAMETER_INDEX): run_id, step, input, external, mdm, final_action, latency_ms, schema_version. All must be present and non-empty where applicable.

## Fail-closed propagation (H4)

- Condition: Exception in propose, update_kill_switch, or modulate.
- Expected: Final decision is safe (allowed=False or action=HOLD/STOP); context or packet can carry fail_closed=True where defined by cores.
