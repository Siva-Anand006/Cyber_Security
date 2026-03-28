# System Architecture

## Flow

```
auth_logs.csv
     │
     ▼
[log_generator.py]  →  Generates synthetic events (normal + malicious)
     │
     ▼
[detection_rules.py]  →  Applies rule signatures; returns alert list
     │
     ▼
[risk_engine.py]  →  Aggregates alerts per user; computes weighted risk score
     │
     ▼
[alert_engine.py]  →  Orchestrates above; deduplicates; saves alerts.csv
     │
     ▼
[app.py]  →  Streamlit dashboard consuming alerts.csv + auth_logs.csv
```

## Component Descriptions

| Module | Responsibility |
|---|---|
| `src/log_generator.py` | Generates synthetic auth events and six attack scenarios |
| `src/detection_rules.py` | Stateful rule checks returning structured alert dicts |
| `src/risk_engine.py` | Weighted scoring per user, capped at 100 |
| `src/alert_engine.py` | Orchestration, deduplication, persistence |
| `app.py` | Anlayst dashboard with KPIs, charts, filters, and alert table |

