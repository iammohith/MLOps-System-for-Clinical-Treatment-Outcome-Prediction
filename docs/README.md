# 📚 Knowledge Base & Documentation

<div align="center">

![Type](https://img.shields.io/badge/Type-Technical_Index-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Living_Document-success?style=for-the-badge)

**Central repository for technical deep-dives, RFCs, and architectural decision records.**

[⬅️ Back to Root](../README.md)

</div>

---

## 1. Document Index

| Document | Category | Description |
| :--- | :--- | :--- |
| **[Model Monitoring](./model_monitoring.md)** | `SPEC` | Architectural proposal for data drift and bias detection (RFC). |
| **[Root Guide](../README.md)** | `GUIDE` | Deployment, Setup, and System Overview. |
| **[Contributing](./CONTRIBUTING.md)** | `POLICY` | Standards for code, security, and medical validation. |

---

## 2. Documentation Architecture

We follow the **Diátaxis** framework to ensure documentation serves its intended purpose:

```mermaid
graph TD
    Docs[Documentation] --> Tutorials[Tutorials]
    Docs --> HowTo[How-to Guides]
    Docs --> Reference[Technical Reference]
    Docs --> Explanation[Architectural Explanation]
    
    style Reference fill:#e3f2fd,stroke:#1565c0
    style Explanation fill:#fff9c4,stroke:#fbc02d
```

### Reference vs. Explanation

- **Sub-READMEs** (e.g., `inference/README.md`) serve as **Refrence** for specific modules.
- **Docs Folder** (this directory) contains **Explanations** and long-term **Specs**.

---

## 3. Writing Standards

All documentation must adhere to the following:

- **Mermaid Diagrams**: Used for any flow or architecture change.
- **Executive Summaries**: Every file must start with "Purpose", "Business Problem", and "Solution".
- **Zero-Trust Context**: Every doc must highlight security boundaries.

---

## 🔮 Future Roadmap

- [ ] **Data Dictionary**: Comprehensive definition of all 1000+ synthetic clinical fields.
- [ ] **Deployment ADRs**: Detailed logs of why specific K8s configurations were chosen.
- [ ] **Medical Validation API**: Swagger UI documentation link.
