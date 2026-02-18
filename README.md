<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# decision-ecosystem-integration-harness

E2E integration layer for the **multi-core decision ecosystem**. This repo is **not a core**; it proves that the five cores work together under contract-first, domain-agnostic invariants.

## Role

- **Single-step pipeline**: propose → ops signal → modulate → PacketV2 → report
- **Invariants (H1–H3 + fullstack E2E)**: schema minor=2 compat, kill-switch dominance, packet trace completeness; H4 fail-closed propagation (planned)
- **SSOT**: Context keys and PacketV2 fields follow `decision-schema` PARAMETER_INDEX

## Cores (dependencies)

| Core | Role |
|------|------|
| decision-schema | Types (Proposal, FinalDecision, PacketV2, Action), compat gate |
| mdm-engine | Proposal generation from state/context |
| ops-health-core | Kill switch → ops_deny_actions, ops_state |
| decision-modulation-core (DMC) | Guards + modulate → FinalDecision |
| evaluation-calibration-core | build_report(packets, expected_schema_minor=2) |

## Schema dependency

- **decision-schema**: `>=0.2,<0.3` (compat: `min_minor=2`, `max_minor=2`)

## Quick start

```bash
# decision-schema is required; if not on PyPI, install from local/git first:
# pip install -e path/to/decision-schema
pip install -e .
# Optional: install other cores locally for full E2E (H2 and full run_one_step)
# pip install -e path/to/mdm-engine path/to/ops-health-core path/to/decision-modulation-core path/to/evaluation-calibration-core
pytest tests/
```

## Layout

- `harness/`: `run_one_step`, `packet_builder`, `redaction`
- `docs/`: ARCHITECTURE, FORMULAS, INTEGRATION_GUIDE, examples
- `tests/`: invariant H1–H3, fullstack E2E, end-to-end smoke

## Invariants (harness-level)

- **H1**: Schema minor=2 compat gate (decision-schema 0.2.x)
- **H2**: Kill-switch dominance: `ops_deny_actions=True` → FinalDecision.allowed=False, action=HOLD
- **H3**: PacketV2 trace completeness (run_id, step, input, external, mdm, final_action, latency_ms, schema_version)
- **H4** (planned): Fail-closed propagation: exception path → safe decision + Packet/fail_closed marker

## License

[Add your license]
