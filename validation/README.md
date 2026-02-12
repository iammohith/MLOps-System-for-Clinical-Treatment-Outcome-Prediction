# 🛡️ Verification System

<div align="center">

![Verified](https://img.shields.io/badge/Status-Verified-green?style=flat-square)
![Quality](https://img.shields.io/badge/Quality-Guaranteed-blue?style=flat-square)

</div>

## 🚪 Safety Checks

To ensure the system is always reliable, we have built a set of automatic safety checks. These checks make sure that everything is working perfectly before the code is released.

---

## ⚡ The Check Checklist

Every time we check the system, it looks at these 5 important areas:

| Area | What it checks |
| :--- | :--- |
| **Files** | Checks if any important code or data files are missing. |
| **Workflow** | Makes sure the step-by-step math process runs correctly. |
| **Containers** | Confirms the system starts up correctly when packaged. |
| **Setup** | Checks if the system layout follows standard rules. |
| **Predictions** | Tests that the system can actually calculate a score. |

---

## 🏃 How to Run Checks

```bash
# The simplest way to check everything at once
make validate

# The detailed technical check
python validation/release_check.py
```

---

## 📜 Standard Checks

We also provide a simpler check (`validate_repo.py`) for computers that don't have all the advanced software installed. This still does a great job of finding common mistakes.
