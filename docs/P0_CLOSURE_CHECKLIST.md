# P0 Closure Checklist — CIA v0.2 DONE

Her madde için: **Dosya → Beklenen durum → Çalıştırılacak test → Beklenen çıktı**.

---

## P0-A — integration-harness: CI YAML

| Öğe | Değer |
|-----|--------|
| **Dosya** | `.github/workflows/ci.yml` |
| **Beklenen** | Çok satırlı, geçerli YAML; "Install test tooling" + "Install decision-schema" + "Install harness" + "Run tests". |
| **Test** | GitHub Actions’ta workflow tetikle (push/PR). |
| **Çıktı** | Workflow parse edilir; job’lar yeşil. |

---

## P0-B — integration-harness: INV0 docs

| Öğe | Değer |
|-----|--------|
| **Dosyalar** | `docs/INTEGRATION_GUIDE.md`, `README.md` |
| **Beklenen** | Örnek state: `signal_0`, `signal_1`, `state_scalar_a`, `state_scalar_b`. README’de sadece "mdm-engine". |
| **Test** | `pytest tests/test_invariant_0_domain_agnosticism.py -v` |
| **Çıktı** | `test_invariant_0_docs_domain_agnostic` PASSED. |

---

## P0-C — mdm-engine: branch / secrets.py

| Öğe | Değer |
|-----|--------|
| **Beklenen** | Default branch’ta `mdm_engine/security/secrets.py` mevcut. |
| **Patch** | GitHub’da default = main; master varsa main’e merge; .gitignore’da `!mdm_engine/security/secrets.py`. |
| **Test** | `python -c "from mdm_engine.security import EnvSecretsProvider; print('ok')"` |

---

## P0-D — mdm-engine: reference model domain-free

| Öğe | Değer |
|-----|--------|
| **Beklenen** | `reference_model_generic.py` generic; legacy `docs/examples/example_domain_legacy_v0/`; INV0 code scan mdm/mdm/ (shim + position_manager hariç). |
| **Test** | `pytest mdm-engine/tests/test_invariant_0_domain_agnosticism.py -v` |
| **Çıktı** | Her iki INV0 test PASSED. |

---

## DONE kriterleri

- [ ] P0-A: Harness CI parse + run.
- [ ] P0-B: Harness INV0 docs PASSED.
- [ ] P0-C: mdm-engine default branch’ta secrets.py var.
- [ ] P0-D: mdm-engine proposal core domain-free; INV0 code PASSED.

Bu koşullar sağlandığında: **CIA v0.2 DONE**; sıradaki faz: Multi-Proposal + Arbitration.

---

## P0 Closure — CIA v0.2 Release Gate (INV0 + CI-0)

**Verdict:** ✅ **P0 CLOSED / CIA v0.2 DONE (release-grade)**.  
Integration harness artık deterministik ve public-safe bir "core integration reference" olarak çalışıyor: (1) **CI workflow hygiene** CI-0 invariant'ı ile byte-level kilitlendi (LF-only, CR=0, Unicode kontrol/embedding karakterleri yok, multi-line workflow; `on:`/`jobs:` satır adreslenebilir), ve her PR/push'ta otomatik çalışıyor; (2) **Domain-agnostic public narrative** INV0 ile README+docs (docs/examples hariç) taranıyor ve yasak lexeme setine karşı **0 ihlal** sağlanıyor; (3) Pipeline "propose → ops-health → modulate → PacketV2 → report" akışı harness testleriyle smoke seviyesinde doğrulanıyor. Bu gate sonrası hedef faz: full-stack CI (core repos) + harness'ta `core-only` ve `full-stack` job ayrımı.

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
