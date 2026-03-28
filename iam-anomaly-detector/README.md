# IAM Anomaly Detector

A Python-based Identity and Access Monitoring system that ingests authentication logs, applies rule-based detection logic to identify suspicious behavior, computes per-user risk scores, and surfaces actionable alerts through a Streamlit analyst dashboard.

---

## Problem Statement

Modern organizations face a growing threat from compromised credentials, insider threats, and account takeovers. This project simulates an IAM monitoring pipeline—processing raw authentication telemetry into structured security alerts—replicating the core workflow of a Security Operations Center (SOC) analyst.

---

## Features

| Feature | Description |
|---|---|
| **Log Generation** | Synthetic authentication logs with six attack patterns |
| **Detection Engine** | Rule-based logic: brute force, impossible travel, off-hours admin, excessive frequency |
| **Risk Scoring** | Per-user weighted risk score (0–100) with risk level classification |
| **Alert Engine** | Deduplication, severity sorting, risk enrichment |
| **Dashboard** | Streamlit + Plotly analyst dashboard with filters |
| **Tests** | Pytest unit tests covering all rules and scoring logic |

---

## Detection Use Cases

- **Brute Force**: >5 failed logins followed by a success → `Critical`
- **Impossible Travel**: Same user authenticates from different countries within 2 hours → `High`
- **Off-Hours Admin Access**: Admin login between 8 PM – 8 AM → `Medium`
- **Excessive Login Frequency**: >25 logins within a 1-hour window → `Medium`

---

## Tech Stack

- **Python 3.10+**
- **pandas** – log parsing and detection logic
- **Streamlit** – analyst dashboard
- **Plotly** – interactive charts
- **Faker** – synthetic data generation
- **pytest** – unit testing

---

## How to Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic logs
python src/log_generator.py

# 4. Run the alert pipeline
PYTHONPATH=. python src/alert_engine.py

# 5. Launch the dashboard
streamlit run app.py

# Optional: Run tests
PYTHONPATH=. pytest tests/
```

---

## Sample Alert Output

```
rule_name: brute_force_attempt
severity: Critical
user_id: user5
description: user5 had 8 failed logins followed by a successful one.
recommendation: Reset credentials and block source IP immediately.
risk_score: 100
risk_level: High
```

---

## Disclaimer

This project uses exclusively synthetic, randomly generated data. No real credentials, users, or systems are involved.
