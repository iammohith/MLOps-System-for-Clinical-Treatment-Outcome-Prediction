# 📈 Evaluation Metrics

<div align="center">

![Format](https://img.shields.io/badge/Format-JSON-black?style=for-the-badge&logo=json)
![DVC](https://img.shields.io/badge/Status-Tracked-945DD6?style=for-the-badge&logo=dvc&logoColor=white)
![Goal](https://img.shields.io/badge/Optimization-Minimize_RMSE-green?style=for-the-badge)

**Quantitative performance reports of the trained models.**
*Tracked, diffable, and automated.*

[⬅️ Back to Root](../README.md)

</div>

---

## 1. Executive Overview

### Purpose

This directory contains the output of the model evaluation stage (`training/evaluate.py`). It provides a standardized, machine-readable report of how well the model predicts clinical outcomes on unseen test data.

### Business Problem

* **Subjective Evaluation**: "It looks good" is not a scientific measure of model quality.
* **Invisible Regressions**: Without tracked metrics, a code change might improve speed but secretly degrade accuracy by 10%.
* **Comparison Hell**: Comparing two models (e.g., "Random Forest" vs "XGBoost") is difficult without a unified metric schema.

### Solution

* **Unified Schema**: All models must output a `scores.json` with specific keys (`rmse`, `mae`, `r2`).
* **Git Integration**: Because these are small text files, they are committed to Git, allowing for `git diff` to show performance changes over time.
* **DVC Integration**: DVC recognizes this file as a metric, enabling `dvc metrics diff`.

### Architectural Positioning

This is the **Report Layer**. It is produced by the *Evaluation Stage* and consumed by the *Human Reviewer* (or automated CI/CD gates).

---

## 2. Directory Contents

| File | Description | Schema |
| :--- | :--- | :--- |
| `scores.json` | Key Performance Indicators (KPIs) calculated on the held-out test set (20% split). | JSON |

---

## 3. Metric Definitions

We use standard regression metrics to quantify clinical prediction accuracy.

### RMSE (Root Mean Squared Error)

* **Formula**: $\sqrt{\frac{1}{n}\sum(y_{true} - y_{pred})^2}$
* **Interpretation**: The standard deviation of the prediction errors. Penalizes large outliers heavily.
* **Clinical Relevance**: Large errors in dosage prediction are dangerous. RMSE is our **Primary Metric**.
* **Goal**: Minimize (Closer to 0 is better).

### MAE (Mean Absolute Error)

* **Formula**: $\frac{1}{n}\sum|y_{true} - y_{pred}|$
* **Interpretation**: The average absolute difference between the predicted improvement score and the actual score.
* **Clinical Relevance**: Easier to explain to doctors ("The score is typically off by 0.5 points").
* **Goal**: Minimize (Closer to 0 is better).

### R² (Coefficient of Determination)

* **Formula**: $1 - \frac{SS_{res}}{SS_{tot}}$
* **Interpretation**: The proportion of variance in the dependent variable that is predictable from the independent variables.
* **Goal**: Maximize (Closer to 1.0 is better).

---

## 4. Usage Guide

### Human Review

Open `metrics/scores.json` to see the latest run results:

```json
{
  "rmse": 0.4321,
  "mae": 0.3105,
  "r2": 0.8910,
  "test_samples": 200
}
```

### Automated Comparison (DVC)

To see how the current workspace passes/fails against the main branch:

```bash
dvc metrics diff main
```

**Example Output:**

```
Path                 Metric    Value    Change
metrics/scores.json  rmse      0.4321   -0.0102  (Improved)
metrics/scores.json  r2        0.8910   +0.0050  (Improved)
```

### CI/CD Gating (Conceptual)

A release gate script typically checks this file:

```python
# Example Gate Logic
if metrics['rmse'] > 0.5:
    raise ValueError("Model performance below threshold (RMSE > 0.5). Deployment Blocked.")
```
