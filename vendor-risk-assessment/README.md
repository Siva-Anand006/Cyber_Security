# Vendor Risk Assessment

A Python-based Third-Party Cyber Risk Assessment Tool that evaluates vendor cybersecurity risk using structured inputs and produces a risk score, risk category, and mitigation recommendations.

This project simulates how organizations assess vendor security posture before granting access to systems or data — directly aligned with **GRC, Third-Party Risk Management (TPRM), and Vendor Risk Analyst** roles.

---

## Problem Statement

Third-party vendors are one of the largest sources of cybersecurity risk in modern organizations. When a vendor is granted access to systems or sensitive data, the organization inherits that vendor's security posture. Without a structured evaluation process, organizations face data breaches, regulatory violations, and operational disruption.

This tool provides a transparent, rule-based framework for evaluating vendor risk before onboarding.

---

## Features

| Feature | Description |
|---|---|
| **Vendor Input Form** | Manually assess any vendor with 6 key attributes |
| **Risk Scoring Engine** | Weighted rule-based scoring system (0–100) |
| **Risk Level Classification** | Low / Medium / High / Critical |
| **Recommendation Engine** | Actionable, factor-based remediation steps |
| **Portfolio View** | Assess all sample vendors at once |
| **Visualizations** | Bar charts, pie chart, and risk heatmap (Plotly) |
| **Unit Tests** | 10 pytest tests covering scoring and classification |

---

## Risk Scoring Logic

| Risk Factor | Score Added |
|---|---|
| High-risk country (RU, CN, KP, IR, BY) | +20 |
| No compliance certification | +30 |
| Admin access level | +40 |
| Write access level | +15 |
| High data sensitivity | +30 |
| Medium data sensitivity | +15 |
| High business criticality | +20 |
| Medium business criticality | +10 |

**Risk Levels:**
- 0–30 → Low
- 31–60 → Medium
- 61–80 → High
- 81–100 → Critical

---

## Tech Stack

- **Python 3.10+**
- **pandas** – data processing
- **Streamlit** – interactive dashboard
- **Plotly** – charts and heatmap
- **pytest** – unit testing

---

## How to Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py

# Optional: Run tests
PYTHONPATH=. pytest tests/ -v
```

---

## Example Assessment Output

```
Vendor: EpsilonData Corp
Country: IN
Access: Admin | Sensitivity: High | Compliance: None | Criticality: High

Risk Score: 100 / 100
Risk Level: Critical

Triggered Factors:
  +40 pts — Vendor has Admin-level access
  +30 pts — No compliance certification
  +30 pts — High data sensitivity
  +20 pts — High business criticality

Recommendations:
  1. Apply the principle of least privilege.
  2. Require SOC2 or ISO27001 certification.
  3. Enforce encryption and strict access controls.
  4. Escalate to CISO — do not grant access until resolved.
```

---

## Disclaimer

This project uses only synthetic vendor data. No real organizations or credentials are represented.
