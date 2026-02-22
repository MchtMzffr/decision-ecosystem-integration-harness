<!--
Decision Ecosystem — decision-ecosystem-integration-harness
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# P0 Closure Checklist — CIA v0.2 DONE

For each item: **File → Expected state → Test to run → Expected output**.

---

## P0-A — integration-harness: CI YAML

| Item | Value |
|------|--------|
| **File** | `.github/workflows/ci.yml` |
| **Expected** | Multi-line, valid YAML; "Install test tooling" + "Install decision-schema" + "Install harness" + "Run tests". |
| **Test** | Trigger workflow in GitHub Actions (push/PR). |
| **Output** | Workflow parses; jobs green. |

---

## P0-B — integration-harness: INV0 docs

| Item | Value |
|------|--------|
| **Files** | `docs/INTEGRATION_GUIDE.md`, `README.md` |
| **Expected** | Example state: `signal_0`, `signal_1`, `state_scalar_a`, `state_scalar_b`. README only references "mdm-engine". |
| **Test** | `pytest tests/test_invariant_0_domain_agnosticism.py -v` |
| **Output** | `test_invariant_0_docs_domain_agnostic` PASSED. |

---

## P0-C — mdm-engine: branch / secrets.py

| Item | Value |
|------|--------|
| **Expected** | `mdm_engine/security/secrets.py` present on default branch. |
| **Patch** | On GitHub default = main; if master exists merge to main; in .gitignore add `!mdm_engine/security/secrets.py`. |
| **Test** | `python -c "from mdm_engine.security import EnvSecretsProvider; print('ok')"` |

---

## P0-D — mdm-engine: reference model domain-free

| Item | Value |
|------|--------|
| **Expected** | `reference_model_generic.py` generic; legacy under `docs/examples/example_domain_legacy_v0/`; INV0 code scan mdm/mdm/ (excluding shim + position_manager). |
| **Test** | `pytest mdm-engine/tests/test_invariant_0_domain_agnosticism.py -v` |
| **Output** | Both INV0 tests PASSED. |

---

## DONE criteria

- [ ] P0-A: Harness CI parse + run.
- [ ] P0-B: Harness INV0 docs PASSED.
- [ ] P0-C: mdm-engine default branch has secrets.py.
- [ ] P0-D: mdm-engine proposal core domain-free; INV0 code PASSED.

When these conditions are met: **CIA v0.2 DONE**; next phase: Multi-Proposal + Arbitration.

---

## P0 Closure — CIA v0.2 Release Gate (INV0 + CI-0)

**Verdict:** ✅ **P0 CLOSED / CIA v0.2 DONE (release-grade)**.  
The integration harness now runs as a deterministic, public-safe "core integration reference": (1) **CI workflow hygiene** is locked at byte level by the CI-0 invariant (LF-only, CR=0, no Unicode control/embedding characters, multi-line workflow; `on:`/`jobs:` lines addressable), and runs automatically on every PR/push; (2) **Domain-agnostic public narrative** is enforced by INV0: README and docs (excluding docs/examples) are scanned and **0 violations** against the prohibited lexeme set; (3) The pipeline flow "propose → ops-health → modulate → PacketV2 → report" is validated at smoke level by harness tests. After this gate, the target phase is: full-stack CI (core repos) + separation of `core-only` and `full-stack` jobs in the harness.

**Evidence (raw):**
- CI workflow: [.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/master/.github/workflows/ci.yml)
- CI-0 invariant: [tests/test_invariant_ci_0_workflow_hygiene.py](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/master/tests/test_invariant_ci_0_workflow_hygiene.py)
- INV0 docs: [tests/test_invariant_0_domain_agnosticism.py](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/master/tests/test_invariant_0_domain_agnosticism.py)
- P0 checklist (this doc): [docs/P0_CLOSURE_CHECKLIST.md](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/master/docs/P0_CLOSURE_CHECKLIST.md)

**Gate commands:**
```bash
pytest tests/test_invariant_ci_0_workflow_hygiene.py -v   # CI-0
pytest tests/test_invariant_0_domain_agnosticism.py -v     # INV0 docs
pytest tests/ -v                                           # full smoke
```
