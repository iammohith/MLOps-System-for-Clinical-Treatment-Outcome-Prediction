# Model Monitoring — Conceptual Design

## Overview

This document describes how model monitoring could be implemented for the Clinical Treatment Outcome Prediction system. It covers data drift detection, prediction drift monitoring, and operational considerations.

> **Disclaimer**: This system predicts patient treatment outcome scores to support clinical research, quality analysis, and exploratory analytics. It does not provide diagnostic or treatment recommendations.

---

## What Is Implemented

### Operational Monitoring (Active)

The following metrics are actively tracked via Prometheus:

| Metric | Type | Description |
|--------|------|-------------|
| `api_request_total` | Counter | Total API requests by method, endpoint, status |
| `api_prediction_total` | Counter | Total predictions served |
| `api_prediction_errors_total` | Counter | Total prediction errors |
| `api_request_duration_seconds` | Histogram | Request latency distribution |
| `model_info` | Gauge | Model version label |

These are scraped by Prometheus every 15 seconds and visualized in Grafana dashboards.

---

## What Is NOT Implemented (and Why)

### 1. Data Drift Detection

**What it would do**: Detect when incoming prediction requests differ statistically from training data distribution.

**Methods that could be used**:

- **Population Stability Index (PSI)**: Measures shift between training and serving distributions. PSI > 0.2 indicates significant drift.
- **Kolmogorov-Smirnov (KS) Test**: Non-parametric test for distribution changes in numeric features.
- **Chi-Square Test**: For categorical feature distribution changes.

**Why not implemented**:

- Requires a persistent store of prediction inputs (database or feature store)
- Needs a reference distribution snapshot from training data
- Adds infrastructure complexity (scheduling, alerting, storage)
- Current dataset is static (1000 rows) — drift is not expected in a research context

**Safe alternative**: Log prediction inputs to a timestamped CSV and periodically run manual distribution comparisons.

### 2. Prediction Drift Monitoring

**What it would do**: Track if prediction distribution shifts over time even if input distribution stays stable.

**Why not implemented**:

- Requires ground truth labels (actual Improvement_Score) to detect concept drift
- In a research context, ground truth may not be available for weeks/months
- Without ground truth, only proxy metrics (prediction mean, variance) can be tracked

**Safe alternative**: Add a Prometheus gauge tracking rolling prediction mean and variance. Alert if prediction mean shifts > 1 standard deviation from training set mean.

### 3. Feature Importance Drift

**What it would do**: Track if model's reliance on features changes across retraining cycles.

**Why not implemented**: Requires multiple model versions and automated comparison infrastructure.

---

## Recommended Future Implementation

If this system moves toward production, the following should be implemented in order:

1. **Prediction logging** → Store all prediction requests/responses with timestamps
2. **PSI monitoring** → Weekly PSI calculation for top features
3. **Prediction distribution tracking** → Rolling mean/variance gauge in Prometheus
4. **Ground truth collection** → Periodic feedback loop for actual outcomes
5. **Automated retraining trigger** → If PSI > 0.2 on any feature, trigger retraining pipeline

---

## Architecture for Future Drift Detection

```
Prediction Request → API → Model → Response
                      ↓
              Prediction Logger
                      ↓
              Feature Store / DB
                      ↓
           Scheduled Drift Analysis
                      ↓
              PSI / KS Calculation
                      ↓
            Alert if threshold exceeded
                      ↓
           Trigger Retraining Pipeline
```

This architecture would require:

- A persistent store (PostgreSQL or similar)
- A scheduler (cron or Airflow)
- An alerting mechanism (Prometheus AlertManager)
- A retraining orchestrator (DVC pipeline trigger)
