# 📊 Observability & Telemetry

<div align="center">

![Prometheus](https://img.shields.io/badge/Prometheus-TSDB-E6522C?style=flat-square&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=flat-square&logo=grafana)
![Uptime](https://img.shields.io/badge/SLA-99.9%25-green?style=flat-square)

</div>

## 🔭 Monitoring Architecture

This repository provides a production-honest observability suite, tracking the health and performance of clinical outcome inferences in real-time.

### 📈 Service Level Indicators (SLIs)

| Category | Metric Name | Purpose |
| :--- | :--- | :--- |
| **Traffic** | `api_request_total` | Tracks system load and endpoint popularity. |
| **Latency** | `api_request_duration_seconds` | High-fidelity histograms for p95/p99 latency. |
| **Errors** | `api_prediction_errors_total` | Real-time visibility into model/preprocessor failures. |
| **Metadata** | `model_info` | Tracks which model version is currently in-flight. |

---

## 🎛️ Grafana Dashboards

We provide a pre-configured dashboard at `monitoring/grafana/dashboards/api_dashboard.json`.

### Visualization Pillars

1. **Request Rate**: Time-series view of method/status distribution.
2. **Latency Quantiles**: Visual proof of millisecond responsiveness.
3. **Error Concentration**: Immediate identification of invalid record spikes.
4. **Version Tracking**: Confirmation of the active DVC model hash.

---

## 🏃 Deployment

```bash
# Part of the Docker stack
docker compose -f infra/docker/docker-compose.yml up prometheus grafana
```

### 🔐 Credentials

* **URL**: `http://localhost:3000`
* **Default User**: `admin`
* **Default Pass**: `mlops2024`

---

## 🛡️ Best Practices Enforced

* **Autodiscovery**: Prometheus is pre-configured to scrape the `inference-api` container within the internal Docker bridge network.
* **Persistence**: Dashboards are managed as code to ensure 1:1 parity between local development and production observability.
