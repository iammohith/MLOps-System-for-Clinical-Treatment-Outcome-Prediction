# 📦 Model Artifacts

<div align="center">

![Format](https://img.shields.io/badge/Format-Joblib-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-blue?style=for-the-badge)
![DVC](https://img.shields.io/badge/Versioning-DVC-945DD6?style=for-the-badge&logo=dvc&logoColor=white)

**The immutable, versioned binary output of the training pipeline.**
*Production-ready inference artifacts.*

[⬅️ Back to Root](../README.md)

</div>

---

## 1. Executive Overview

### Purpose

This directory serves as the **Artifact Store** for the trained machine learning models. The files here are the "Deliverable" of the MLOps process—binary objects that encapsulate the learned intelligence from the clinical data.

### Business Problem

* **Model Drift**: Without versioned artifacts, it's impossible to know *which* model is running in production.
* **Reproducibility**: If a model fails in production, engineers need to be able to download the *exact* binary that failed to debug it.
* **Serialization Risks**: Using arbitrary pickle files can lead to remote code execution (RCE) vulnerabilities.

### Solution

* **Immutable Blobs**: Once a model is trained, this file is treated as read-only.
* **Cryptographic Linkage**: DVC links this binary (`.joblib`) to the exact Git commit of the code and the SHA-256 hash of the training data.
* **Safe Serialization**: We use `joblib` (specialized for NumPy arrays) instead of raw `pickle` where possible, though trust boundaries still apply.

### Architectural Positioning

This is the **Interface Layer** between the *Training Pipeline* (Producer) and the *Inference Service* (Consumer).

---

## 2. Directory Contents

| File | Description | Loader |
| :--- | :--- | :--- |
| `model.joblib` | **The Brain**. A serialized `RandomForestRegressor` object containing all trees, nodes, and leaf weights. | `joblib.load()` |

> **Note**: The `preprocessor.joblib` (Scaling/Encoding logic) is stored in `data/processed/` as it is tightly coupled to the data schema, whereas this folder contains the high-level prediction logic.

---

## 3. Versioning & Lineage

The "Five Ws" of any model in this directory are tracked via DVC:

1. **Who** trained it? (Git Author)
2. **What** code was used? (Git Commit SHA)
3. **Where** is the data? (DVC Data Hash)
4. **When** was it trained? (Git Timestamp)
5. **Why** (Parameters)? (`params.yaml` state)

To verify the current model's lineage:

```bash
dvc status models/model.joblib
```

---

## 4. Usage Guide

### Loading in Production (Python)

```python
import joblib
import pandas as pd

# 1. Load the artifact
# NOTE: Ensure scikit-learn version matches training environment
model = joblib.load('models/model.joblib')

# 2. Prepare Input (Must match training schema columns)
input_data = pd.DataFrame([{
    'Age': 45,
    'Dosage_mg': 500.0,
    # ... other features ...
}])

# 3. Predict
score = model.predict(input_data)[0]
return float(score)
```

### Compatibility Matrix

| Dependency | Version Requirement | Reason |
| :--- | :--- | :--- |
| `scikit-learn` | `==1.4.1` | Tree structure serialization format changes between versions. |
| `joblib` | `>=1.3.0` | Compression and persistence format. |
| `numpy` | `>=1.26.0` | Array definition compatibility. |

> **Warning**: Attempting to load this model in an environment with a mismatched `scikit-learn` version will likely raise a `ValueError` or `AttributeError`. Usage of `infra/docker/Dockerfile.inference` ensures environment consistency.
