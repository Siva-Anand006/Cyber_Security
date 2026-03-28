import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.detection_rules import apply_all_rules
from src.risk_engine import calculate_risk_scores

SEVERITY_ORDER = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}


def load_logs(data_dir):
    path = os.path.join(data_dir, "auth_logs.csv")
    if not os.path.exists(path):
        print("No auth_logs.csv found. Run log_generator.py first.")
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def run_alert_engine():
    print("Starting IAM Alert Engine...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    df = load_logs(data_dir)
    if df.empty:
        return pd.DataFrame()

    print(f"Loaded {len(df)} log entries. Running detection rules...")
    raw_alerts = apply_all_rules(df)

    if not raw_alerts:
        print("No alerts generated.")
        return pd.DataFrame()

    # Compute risk scores and merge into alerts
    risk_df = calculate_risk_scores(raw_alerts)
    alerts_df = pd.DataFrame(raw_alerts)

    # Deduplicate: keep worst-severity alert per user+rule combination
    alerts_df["severity_score"] = alerts_df["severity"].map(SEVERITY_ORDER).fillna(0)
    alerts_df = alerts_df.sort_values("severity_score", ascending=False)
    alerts_df = alerts_df.drop_duplicates(subset=["rule_name", "user_id"])

    # Attach risk score
    alerts_df = alerts_df.merge(risk_df[["user_id", "risk_score", "risk_level"]], on="user_id", how="left")

    # Final sort
    alerts_df = alerts_df.sort_values(by=["severity_score", "timestamp"], ascending=[False, False])
    alerts_df = alerts_df.drop(columns=["severity_score"])

    out_path = os.path.join(data_dir, "alerts.csv")
    alerts_df.to_csv(out_path, index=False)
    print(f"Alert engine complete. {len(alerts_df)} unique alerts saved to '{out_path}'.")

    return alerts_df


if __name__ == "__main__":
    run_alert_engine()

