# 📈 Evaluation Metrics

<div align="center">

![JSON](https://img.shields.io/badge/Format-JSON-black?style=for-the-badge&logo=json)
![DVC](https://img.shields.io/badge/Tracked-DVC_Metrics-945DD6?style=for-the-badge)

**Quantitative performance reports of the trained model.**

[⬅️ Back to Root](../README.md)

</div>

---

## 1. Directory Contents

This directory contains the output of the `training/evaluate.py` stage.

| File | Description | Format |
| :--- | :--- | :--- |
| `scores.json` | Key performance indicators (RMSE, MAE, R²) on the test set. | JSON |

---

## 2. Metric Definitions

We use standard regression metrics to quantify clinical prediction accuracy.

### RMSE (Root Mean Squared Error)

* **Formula**: $\sqrt{\frac{1}{n}\sum(y_{true} - y_{pred})^2}$
* **Interpretation**: The standard deviation of the prediction errors. Penalizes large outliers heavily.
* **Goal**: Minimize (Closer to 0 is better).

### MAE (Mean Absolute Error)

* **Formula**: $\frac{1}{n}\sum|y_{true} - y_{pred}|$
* **Interpretation**: The average absolute difference between the predicted improvement score and the actual score.
* **Goal**: Minimize (Closer to 0 is better).

### R² (Coefficient of Determination)

* **Formula**: $1 - \frac{SS_{res}}{SS_{tot}}$
* **Interpretation**: The proportion of variance in the dependent variable that is predictable from the independent variables.
* **Goal**: Maximize (Closer to 1.0 is better).

---

## 3. DVC Integration

These metrics are tracked by DVC to allow for experiment comparison.

```bash
# Compare current run vs main branch
dvc metrics diff main
```

**Example Output:**

```
Path                 Metric    Value    Change
metrics/scores.json  rmse      0.4321   -0.0102
metrics/scores.json  r2        0.8910   +0.0050
```
