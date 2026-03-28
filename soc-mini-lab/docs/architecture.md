# Architecture Overview

## Components

1. **Log Generator (`src/log_generator.py`)**
   - Synthesizes `auth_logs.csv` and `api_logs.csv` to mimic real-world interactions.
   - Outputs: `data/*.csv`
2. **Detection Rule Engine (`src/detection_rules.py`)**
   - Contains signatures for evaluating data points to detect malicious behavior.
3. **Alert Engine (`src/alert_engine.py`)**
   - Ingests raw CSV data and runs it linearly through `detection_rules.py`.
   - Structures alerts into a standard schema (deduplicated, sorted).
4. **Analyst Dashboard (`app.py`)**
   - Renders statistics, charts, and table logs for triage.
5. **Report Generator (`src/report_generator.py`)**
   - Consolidates alerts into natural language analyst reports.
