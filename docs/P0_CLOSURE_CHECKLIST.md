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
