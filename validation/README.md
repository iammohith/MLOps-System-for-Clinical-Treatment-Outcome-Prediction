# 🛡️ Validation System

<div align="center">

![Zero-Trust](https://img.shields.io/badge/Policy-Zero_Trust-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Automated integrity and quality gates.**
*Verified for local execution.*

[⬅️ Back to Root](../README.md)

</div>

---

## ⚡ The "Zero-Trust" Protocol

We do not assume the system is working; we prove it. The validation suite runs authoritative checks before any release.

### Run Verification

```bash
make validate
```

---

## 🔍 What is Checked?

| Category | Description | Status |
| :--- | :--- | :--- |
| **Integrity** | Presence of all mandatory files (Code, Config, Dockerfiles). | ✅ |
| **Pipeline** | Successful execution of DVC stages (repro). | ✅ |
| **Artifacts** | Existence of `model.joblib` and `preprocessor.joblib`. | ✅ |
| **Infrastructure** | Syntax warnings for Docker/K8s (Dry-Run). | ✅ |
| **API Runtime** | Liveness of the Inference API (if running). | ✅ |

> [!IMPORTANT]
> The validation script considers "Environment Blockers" (like missing Docker daemon) as messages, allowing local development validation to proceed.

---

## ❓ Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `Model not found` | Pipeline hasn't run. | Run `make run-pipeline`. |
| `Connection refused` | API isn't running. | Run `make run-api` in another terminal. |
| `Docker not found` | Daemon is stopped. | Start Docker Desktop or ignore if just testing logic. |
