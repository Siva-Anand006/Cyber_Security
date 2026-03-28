# System Architecture

## Flow

```
User Input / sample_vendors.csv
        │
        ▼
[scoring_rules.py]  →  Evaluates each vendor attribute; returns triggered factors + score contributions
        │
        ▼
[risk_engine.py]  →  Aggregates scores; caps at 100; classifies as Low / Medium / High / Critical
        │
        ▼
[recommendation_engine.py]  →  Maps each triggered factor to a specific actionable recommendation
        │
        ▼
[app.py (Streamlit)]  →  Presents results via form, gauge chart, factor list, and portfolio dashboard
```

## Component Descriptions

| Module | Responsibility |
|---|---|
| `src/scoring_rules.py` | Defines and evaluates individual risk factors with weights and explanations |
| `src/risk_engine.py` | Aggregates rule outputs to a capped risk score and risk level |
| `src/recommendation_engine.py` | Maps triggered factors to human-readable mitigation recommendations |
| `src/utils.py` | Loads vendor CSV and batch-scores all vendors |
| `app.py` | Streamlit dashboard with input form, assessment output, and portfolio view |
