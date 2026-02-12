# 📊 System Monitoring

<div align="center">

![Prometheus](https://img.shields.io/badge/Stat%20Tracker-Prometheus-E6522C?style=flat-square&logo=prometheus)
![Grafana](https://img.shields.io/badge/Charts-Grafana-F46800?style=flat-square&logo=grafana)

</div>

## 🔭 Watching the System

This part of the system watches how well the predictions are working in real-time. It helps ensure that the service remains fast and accurate.

### 📈 Important Stats

| Category | What it means |
| :--- | :--- |
| **Usage** | How many people are using the system right now. |
| **Speed** | How many seconds it takes to provide a prediction. |
| **Errors** | If any calculations have failed or been blocked. |
| **Version** | Which version of the AI model is currently active. |

---

## 🎛️ Performance Charts

We have built a dashboard that shows these stats in easy-to-read charts.

1. **Usage Rate**: Shows if the system is getting busy.
2. **Response Time**: Shows if the system is staying fast.
3. **Accuracy Check**: Shows if the math is following expected patterns.

---

## 🏃 How to View

```bash
# Start the monitoring tools
docker compose -f infra/docker/docker-compose.yml up prometheus grafana
```

### 🔐 Access Details

* **Link**: `http://localhost:3000`
* **User**: `admin`
* **Pass**: `mlops2024`

---

## 🛡️ Best Practices

* **Safe Tracking**: The system is set up to automatically find the prediction engine and start watching it.
* **Always Ready**: The charts are saved as part of the code, so they are always ready to use when you start the system.
