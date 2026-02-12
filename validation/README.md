# 🛡️ Authoritative Validation Engine

<div align="center">

![Zero-Trust](https://img.shields.io/badge/Security-Zero%20Trust-black?style=flat-square)
![Quality](https://img.shields.io/badge/Quality-Enforced-green?style=flat-square)
![Compliance](https://img.shields.io/badge/Compliance-DVC--Verified-blue?style=flat-square)

</div>

## 🚪 Post-Remediation Quality Gates

As of the latest Senior Engineer remediation, repository verification is binary. We do not allow "partial" success. The `validation/` directory contains the authoritative logic that guards the release.

---

## ⚡ The Release Decision Matrix

Every release is scrutinized by the `release_check.py` engine across 5 critical vectors.

| Vector | Check | Fail Condition |
| :--- | :--- | :--- |
| **Integrity** | Hash-verify core artifacts. | Missing `.dvc` files or `params.yaml`. |
| **Lifecycle** | `dvc repro` smoke test. | Stale model or broken DAG. |
| **Images** | Multi-stage Docker build. | Compiler error or missing deps. |
| **Manifests** | K8s dry-run validation. | Syntax error or invalid API version. |
| **Hot-Path** | API `/predict` logic check. | Incorrect prediction or timeout. |

---

## 🏃 Authority Commands

```bash
# The One-Step Quality Gate (Recommended)
make validate

# The Technical Deep-Audit
python validation/release_check.py
```

---

## 📜 Legacy Compatibility

The `validate_repo.py` script is maintained for non-Docker environments. It provides **soft-validation** (warnings) but does NOT authorize a production-honest release.

**Rule of Thumb**: If `release_check.py` fails, the repository is BROKEN for external engineers.
