# 📚 Knowledge & Documentation Hub

<div align="center">

![Docs](https://img.shields.io/badge/Format-Markdown-blue?style=flat-square&logo=markdown)
![API](https://img.shields.io/badge/Docs-Swagger/OpenAPI-green?style=flat-square&logo=openai)
![Design](https://img.shields.io/badge/Design-Conceptual--Roadmap-orange?style=flat-square)

</div>

## 🌍 Documentation Ecosystem

This system maintains documentation at three distinct levels of abstraction: **Execution**, **Interface**, and **Concept**.

### 📖 Content Directory

| Resource | Purpose | Format |
| :--- | :--- | :--- |
| **Root README** | System setup & authoritative verification. | Markdown |
| **Interactive API** | Sandbox for testing request validation. | Swagger / OpenAPI |
| **Monitoring Design** | Conceptual roadmap for drift detection. | `model_monitoring.md` |

---

## 🕹️ Interactive API Reference

When the system is running (`make run-pipeline && python -m uvicorn inference.app:app`), developers can access the live sandbox:

**URL**: <http://localhost:8000/docs>

### 🔬 What to Test

* **Schema Rejection**: Send an invalid `Patient_ID` or out-of-range `Age` to observe Pydantic's 422 error logic.
* **Predictive Hot-Path**: Execute a valid POST to verify millisecond-level inference.

---

## 🔮 Future Roadmap

See `docs/model_monitoring.md` for a deep-dive into the conceptual implementation of **Data Drift Detection** using PSI (Population Stability Index) and KS-Tests.
