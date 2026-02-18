<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# P2 DONE — Ecosystem Stabilization Evidence (CIA v0.2)

This sprint stabilized the ecosystem as a contract-first, domain-agnostic decision stack with deterministic safety gates and reproducible integration checks. The contract is pinned to **decision-schema 0.2.x** (`>=0.2,<0.3`), and every core remains **schema-only dependent** (no cross-core imports), with domain examples quarantined under `docs/examples/` and excluded from packaging.

**Last updated:** YYYY-MM-DD (Europe/Istanbul)  
**Last updated (UTC):** YYYY-MM-DDTHH:MM:SSZ  
**Evidence collected from:** GitHub Actions successful runs on main/master.

**Pytest summary format (mandatory):** `X passed, Y failed, Z skipped` — parseable, one line per job.

---

**Evidence chain (CI + invariants):**

Each line is a point-in-time snapshot: branch, commit SHA, and pytest summary from the last green run.

- **decision-schema** — CI + CI-0 hygiene + INV0 (domain-agnostic public surface) + INV2 (no cross-core imports) + PKG-1 (no examples packaged).  
  Actions: https://github.com/MchtMzffr/decision-schema/actions | branch: `main` | commit: `<paste SHA>` | pytest: `<N> passed, 0 failed, 0 skipped`

- **decision-modulation-core (dmc-core)** — CI + CI-0 + INV0 + INV2 + PKG-1; deterministic guard ordering + fail-closed (INVARIANT 3/4).  
  Actions: https://github.com/MchtMzffr/decision-modulation-core/actions | branch: `main` | commit: `<paste SHA>` | pytest: `<N> passed, 0 failed, 0 skipped`

- **ops-health-core** — CI + CI-0 + INV0 + INV2 + PKG-1; kill-switch fail-closed and exception fail-closed verified.  
  Actions: https://github.com/MchtMzffr/ops-health-core/actions | branch: `main` | commit: `<paste SHA>` | pytest: `<N> passed, 0 failed, 0 skipped`

- **evaluation-calibration-core** — CI + CI-0 + INV0/INV2 + PKG-1; report builder and fixed metric key set (INVARIANT 5).  
  Actions: https://github.com/MchtMzffr/evaluation-calibration-core/actions | branch: `main` | commit: `<paste SHA>` | pytest: `<N> passed, 0 failed, 0 skipped`

- **mdm-engine** — CI + CI-0 + INV0 (exclude=0, core-only scan) + INV2 + PKG-1 + PKG-2; legacy quarantined to `docs/examples/`, packaging `mdm_engine.mdm` + `mdm_engine.security`, **skip=0**.  
  Actions: https://github.com/MchtMzffr/mdm-engine/actions | branch: `main` | commit: `<paste SHA>` | pytest: `19 passed, 0 failed, 0 skipped`

- **decision-ecosystem-integration-harness** — CI split: **core_only** (`-m "not fullstack"`, skip=0) and **full_stack** (all cores + fullstack invariants + E2E report).  
  Actions: https://github.com/MchtMzffr/decision-ecosystem-integration-harness/actions | branch: `master` | commit: `<paste SHA>` | pytest core_only: `6 passed, 0 failed, 0 skipped` | pytest full_stack: `<N> passed, 0 failed, 0 skipped`

---

**P2 DONE definition:** All listed repositories show green CI runs and pass their invariant gates (CI-0, INV0, INV2, PKG-1; plus core-specific invariants) under the pinned contract range `decision-schema>=0.2,<0.3`.

**How to refresh:** For each repo, open Actions → last successful run → copy commit SHA and pytest summary in the format **`X passed, Y failed, Z skipped`** into the placeholders above. Then set **Last updated** (Europe/Istanbul) and **Last updated (UTC)** (ISO 8601, e.g. `2026-02-18T12:00:00Z`).
