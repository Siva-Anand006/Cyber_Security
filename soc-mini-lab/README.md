# Threat Detection & SOC Mini-Lab

I built a simulated SOC monitoring pipeline that ingests system activity logs, applies detection logic for suspicious behavior, and surfaces security alerts through an analyst dashboard.

## Overview
This project maps theoretical concepts to real-world security operations. It demonstrates core analytical rigor by processing synthetic raw telemetry into actionable intelligence, mirroring the responsibilities of a Junior Detection Analyst or SOC Analyst.

### Why This Project?
- **Backend Developer Experience**: Applying log parsing, API generation, Python logic, and structured debugging.
- **Systems Engineering Master's**: System thinking, risk analysis, and structured problem solving across multiple components.
- **Research Assistant Work**: Analytical rigor, experimentation with detection logic, and thorough documentation.
- **Procurement Analyst Role**: Risk awareness, governance mindset, and contextualizing business impact through incident reports.

## Features
- **Synthetic Log Generation**: Generates `auth_logs` and `api_logs` with simulated attack signatures (brute force, impossible travel, off-hours access, API bursts).
- **Detection Engine**: Rule-based Python detection engine assigning severity (Critical, High, Medium, Low).
- **Alert Engine**: Dedupes and sorts alerts for analyst triage.
- **Analyst Dashboard**: A Streamlit frontend for viewing alert trends, top suspicious IPs, and incident drill-downs.
- **Report Generation**: Outputs a plain-English analyst incident summary.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Generate logs:
   ```bash
   python src/log_generator.py
   ```

3. Run the alert detection engine:
   ```bash
   python src/alert_engine.py
   ```

4. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

5. Generate incident reports:
   ```bash
   python src/report_generator.py
   ```

## Architecture

*(Architecture Diagram Placeholder - Place `architecture.png` here)*

See `docs/architecture.md` for a full breakdown.
