# 📄 Technical Spec: Advanced Model Monitoring

<div align="center">

![Status](https://img.shields.io/badge/Status-RFC_(Request_For_Comments)-orange?style=for-the-badge)
![Scope](https://img.shields.io/badge/Scope-Future_Architecture-blue?style=for-the-badge)

**Architectural proposal for Data Drift, Concept Drift, and Bias Detection.**

[⬅️ Back to Docs](./README.md)

</div>

---

## 1. Executive Summary

### Objective

Transition from **Operational Monitoring** (System Health, Latency) to **ML Observability** (Data Quality, Model Decay).

### Current State (v1.0)

- **Metrics**: Prometheus tracks `api_prediction_total` and `latency`.
- **Gap**: No visibility into *why* a model might be failing (e.g., input distribution shift).

### Proposed State (v2.0)

- **Drift Detection**: Automated alerts when input data diverges from training baseline.
- **Bias Auditing**: Real-time tracking of fairness metrics across protected groups (Gender/Age).

---

## 2. Target Architecture

The proposed architecture introduces a "Store & Analyze" pattern using an asynchronous sidecar.

```mermaid
graph TD
    Client -->|POST /predict| API[Inference API]
    API -->|Log Payload| Queue[Message Queue (Redis/Kafka)]
    API -->|Response| Client
    
    subgraph "Async Analysis Layer"
        Queue -->|Consume| Worker[Drift Analyzer Worker]
        Worker -->|Fetch Baseline| FeatureStore[(Training Reference)]
        
        Worker -->|Compute Metric| PSI[PSI Calculator]
        PSI -->|Metric > 0.2| Alert[PagerDuty/Slack]
        PSI -->|Save Metric| TimeSeriesDB[Prometheus]
    end
    
    style API fill:#e3f2fd,stroke:#1565c0
    style Worker fill:#fff9c4,stroke:#fbc02d
    style Alert fill:#ffebee,stroke:#c62828
```

---

## 3. Metrics Specification

### A. Data Drift (Population Stability Index - PSI)

- **Definition**: Measures the difference in distribution between the serving data ($S$) and training data ($T$) for a given feature.
- **Thresholds**:
  - $PSI < 0.1$: No significant drift.
  - $PSI \ge 0.2$: **Critical Alert**. Retraining required.

### B. Concept Drift (Prediction Shift)

- **Definition**: Change in the distribution of the predicted target variable (`Improvement_Score`).
- **Proxy**: Since ground truth comes late, we monitor the *Prediction Mean* and *Variance* over time windows (e.g., 24h rolling).

---

## 4. Implementation Stages

### Phase 1: Payload Logging (Q2 2026)

**Goal**: Persist every prediction request/response for offline analysis.

- **Tech**: JSON-Lines (JSONL) rotation on shared volume or S3 upload.

### Phase 2: Scheduled Analysis (Q3 2026)

**Goal**: Daily batch job to compute PSI.

- **Tech**: Airflow DAG running `deepchecks` or `evidently` suites.

### Phase 3: Real-Time Intervention (Q4 2026)

**Goal**: Automated circuit breakers.

- **Logic**: If $PSI > 0.5$ for 1 hour, fallback to a "Safe Mode" (heuristic rule-based) model.

---

## 5. Alternatives Considered

| Approach | Pros | Cons | Decision |
| :--- | :--- | :--- | :--- |
| **In-App Calculation** | Simple, no extra infra. | Increases API latency. Blocks main thread. | ❌ Rejected |
| **Async Sidecar** | Decoupled, scalable. | Adds complexity (Queue, Worker). | ✅ Accepted |
| **Vendor Solution** | "Magical" integration. | Vendor lock-in, data privacy concerns. | ❌ Rejected |
