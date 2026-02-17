# CIA v0.2 P0 Doğrulama Raporu

**Tarih:** GitHub raw içerik doğrulaması  
**Repolar:** decision-ecosystem-integration-harness (master), mdm-engine (main)

---

## A) integration-harness — CI YAML

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| Dosya çok satırlı, parse edilebilir yapıda mı? | **OK** | `name: CI`, `on:`, `jobs:`, `test:`, `steps:` ayrı satırlarda; adımlar: Checkout, Set up Python, Install test tooling, Install decision-schema, Install harness, Run tests. |
| Tek satıra sıkışmış mı? | **Hayır** | Raw’da satırlar ayrı. |
| **A kararı** | **P0-A KAPALI** | Workflow yapısı doğru. GitHub Actions’ta tetikleyip job’ın yeşil düştüğünü ek doğrula. |

---

## B) integration-harness — README "ami-engine" sızıntısı

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| "ami-engine" veya "(ami-engine)" var mı? | **Yok** | README’de sadece "mdm-engine" (Cores tablosu). |
| **B kararı** | **P0-B KAPALI** | INV0 docs ile uyumlu. |

---

## C) integration-harness — Public code domain key mapping

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| INTEGRATION_GUIDE örnek state? | **OK** | `signal_0`, `signal_1`, `state_scalar_a`, `state_scalar_b` kullanılıyor. |
| run_one_step.py `_state_to_features`? | **OK** | Sadece `features = dict(state)` ve `now_ms` context’ten; `mid` / `imbalance` / `depth` / `spread_bps` yok. |
| **C kararı** | **P0-C KAPALI** | Domain-agnostic passthrough; forbidden lexeme yok. |

---

## D) mdm-engine — reference_model.py domain-free shim

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| reference_model.py içeriği? | **OK** | Sadece re-export: `from ... reference_model_generic import compute_proposal_reference, compute_proposal_private` ve `__all__`. |
| mid, imbalance, depth, spread, quote, bid, ask vb. var mı? | **Yok** | Dosyada yalnızca "reference_model_generic", "compute_proposal_reference", "compute_proposal_private", "docs/examples". |
| **D kararı** | **P0-D KAPALI** | Core’da domain lexeme yok. |

---

## E) mdm-engine — INV0 core code scan

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| Core code taraması (mdm_engine/mdm/) var mı? | **Evet** | test_invariant_0_core_code_domain_agnostic mevcut. |
| reference_model.py taranıyor mu? | **Evet** | Exclude sadece position_manager.py; reference_model.py artık taranıyor ve temiz. |
| **E kararı** | **P0-E KAPALI** | Forbidden lexeme = 0 (position_manager hariç; ileride quarantine). |

---

## Ek: mdm-engine default branch / secrets.py

| Kontrol | Sonuç | Kanıt |
|--------|--------|-------|
| main’de mdm_engine/security/secrets.py var mı? | **Evet** | Raw’da SecretsProvider, EnvSecretsProvider tanımlı. |
| **P0-C (branch)** | **KAPALI** | secrets.py main’de mevcut. |

---

## P0 DONE Gate özeti

| Repo | Koşul | Durum |
|------|--------|--------|
| integration-harness | CI YAML geçerli, INV0 docs, run_one_step domain-free | **OK** |
| integration-harness | pytest tests/ → PASS (H2 skip kabul) | Yerelde 7 passed |
| mdm-engine | reference_model.py domain-free, INV0 code scan | **OK** |
| mdm-engine | secrets.py main’de | **OK** |
| mdm-engine | pytest -q → PASS | Yerelde 15 passed, 1 skipped |

---

## Sonuç

**CIA v0.2 P0 checklist GitHub raw’a göre kapalı.**

- A–E maddeleri doğrulandı.
- Harness ve mdm-engine için belirtilen dosyalar beklenen içerikte.
- Son adım: GitHub Actions’ta harness workflow’unu bir kez tetikleyip job’ın yeşil düştüğünü görmek (CI parse + run).
