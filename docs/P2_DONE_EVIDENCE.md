# P2 DONE — Ecosystem Stabilization Evidence (CIA v0.2)

This sprint stabilized the ecosystem as a contract-first, domain-agnostic decision stack with deterministic safety gates and reproducible integration checks. The contract is pinned to **decision-schema 0.2.x** (`>=0.2,<0.3`), and every core remains **schema-only dependent** (no cross-core imports), with domain examples quarantined under `docs/examples/` and excluded from packaging.

**Evidence chain (CI + invariants):**

- **decision-schema**: CI + CI-0 hygiene + INV0 (domain-agnostic public surface) + INV2 (no cross-core imports) + PKG-1 (no examples packaged).  
  Actions: https://github.com/MchtMzffr/decision-schema/actions — pytest summary: *[paste latest run: N passed, 0 skipped]*

- **decision-modulation-core (dmc-core)**: CI + CI-0 + INV0 + INV2 + PKG-1; deterministic guard ordering + fail-closed enforced by tests (INVARIANT 3/4).  
  Actions: https://github.com/MchtMzffr/decision-modulation-core/actions — pytest summary: *[paste latest run]*

- **ops-health-core**: CI + CI-0 + INV0 + INV2 + PKG-1; kill-switch fail-closed and exception fail-closed behavior verified.  
  Actions: https://github.com/MchtMzffr/ops-health-core/actions — pytest summary: *[paste latest run]*

- **evaluation-calibration-core**: CI + CI-0 + INV0/INV2 + PKG-1; report builder and fixed metric key set enforced (INVARIANT 5).  
  Actions: https://github.com/MchtMzffr/evaluation-calibration-core/actions — pytest summary: *[paste latest run]*

- **mdm-engine**: CI + CI-0 + INV0 (exclude=0, core-only scan) + INV2 + PKG-1 + PKG-2; legacy modules quarantined to `docs/examples/`, packaging restricted to `mdm_engine.mdm` and `mdm_engine.security`, and test suite is **skip=0**.  
  Actions: https://github.com/MchtMzffr/mdm-engine/actions — pytest summary: *[paste latest run: 19 passed, 0 skipped]*

- **decision-ecosystem-integration-harness**: CI split into **core_only** and **full_stack** jobs; core_only runs with schema+harness only (`-m "not fullstack"`) with **skip=0**; full_stack installs all cores and runs fullstack-marked invariants and E2E report assertions.  
  Actions: https://github.com/MchtMzffr/decision-ecosystem-integration-harness/actions — pytest summaries: core_only=*[6 passed, 3 deselected]*; full_stack=*[paste latest full_stack job]*

**P2 DONE definition:** All listed repositories show green CI runs and pass their invariant gates (CI-0, INV0, INV2, PKG-1; plus core-specific invariants such as DMC determinism/fail-closed, ops fail-closed, eval metric key set) under the pinned contract range `decision-schema>=0.2,<0.3`.
