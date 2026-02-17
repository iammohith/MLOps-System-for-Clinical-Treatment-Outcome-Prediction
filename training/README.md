# 🧠 Model Training & Evaluation Logic

<div align="center">

![Scikit-Learn](https://img.shields.io/badge/Model-RandomForest-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Metrics](https://img.shields.io/badge/Metrics-RMSE_MAE_R2-blue?style=for-the-badge)

**The core algorithmic engine for the clinical prediction system.**

[⬅️ Back to Root](../README.md)

</div>

---

## 1. Module Overview

This directory contains the pure Python logic for training the predictive model and evaluating its performance. While these scripts are orchestrated by **DVC** (see `../pipelines/`), they are designed to be standalone, modular, and testable.

### Key Scripts

| Script | Purpose | Output |
| :--- | :--- | :--- |
| `train.py` | Trains a **Random Forest Regressor** on processed data. | `models/model.joblib` |
| `evaluate.py` | Calculates error metrics on the held-out test set. | `metrics/scores.json` |

---

## 2. Technical Implementation `train.py`

### Algorithm Selection

We utilize a **Random Forest Regressor** (Ensemble Method) for the following reasons:

* **Non-Linearity**: Efficiently captures complex interactions between drug dosage and patient age.
* **Robustness**: Less prone to overfitting than Decision Trees.
* **Interpretability**: Feature importances are logged to stdout for clinical validation.

### Configuration

Hyperparameters are injected from `params.yaml` (Section `model`):

* `n_estimators`: Number of trees.
* `max_depth`: Prevention of overfitting.
* `min_samples_split`: Leaf node granularity.

### Resource Safety

* **Concurrency**: Uses `os.cpu_count()` or `N_JOBS` env var to limit parallelism (critical for containerized execution).
* **Memory**: Loads data efficiently using Pandas.

---

## 3. Evaluation Strategy `evaluate.py`

We assess model quality using three key regression metrics:

1. **RMSE (Root Mean Squared Error)**: Penalizes large errors heavily. Critical for medical dosage/score safety.
2. **MAE (Mean Absolute Error)**: The average magnitude of errors. Easier to interpret for clinicians (e.g., "The score is off by 0.5 points on average").
3. **R² (Coefficient of Determination)**: Explains how much variance the model captures.

### Metric Output

Results are serialized to `metrics/scores.json`:

```json
{
  "rmse": 0.4321,
  "mae": 0.3105,
  "r2": 0.8910,
  "test_samples": 200
}
```

---

## 4. Usage Guide

### Automated (Recommended)

Run the full pipeline via DVC:

```bash
dvc repro
```

### Manual (Debugging)

You can run the scripts directly if the data is already processed:

```bash
# 1. Train
python training/train.py

# 2. Evaluate
python training/evaluate.py
```

*Note: Scripts expect `params.yaml` to be present in the root directory.*
