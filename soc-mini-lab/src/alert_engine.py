import pandas as pd
from src.detection_rules import apply_all_rules
import os
import sys

# Ensure proper module loading if run from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SEVERITY_MAPPING = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

def load_data(data_dir):
    auth_path = os.path.join(data_dir, "auth_logs.csv")
    api_path = os.path.join(data_dir, "api_logs.csv")
    
    auth_df = pd.read_csv(auth_path) if os.path.exists(auth_path) else pd.DataFrame()
    api_df = pd.read_csv(api_path) if os.path.exists(api_path) else pd.DataFrame()
    
    if not auth_df.empty:
        auth_df['timestamp'] = pd.to_datetime(auth_df['timestamp'])
    if not api_df.empty:
        api_df['timestamp'] = pd.to_datetime(api_df['timestamp'])
        
    return auth_df, api_df

def run_alert_engine():
    print("Starting SOC Alert Engine...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    auth_df, api_df = load_data(data_dir)
    
    if auth_df.empty and api_df.empty:
        print("No log data found to process.")
        return pd.DataFrame()
        
    print(f"Loaded {len(auth_df)} auth logs and {len(api_df)} api logs. Running detection rules...")
    raw_alerts = apply_all_rules(auth_df, api_df)
    
    if not raw_alerts:
        print("No alerts generated. Environment is clear.")
        return pd.DataFrame()
        
    alerts_df = pd.DataFrame(raw_alerts)
    
    # Deduplicate alerts based on rule_name, affected_user, and source_ip, keeping the most recent
    alerts_df = alerts_df.sort_values('timestamp', ascending=False)
    alerts_df = alerts_df.drop_duplicates(subset=['rule_name', 'affected_user', 'source_ip'])
    
    # Sort by severity and recency
    alerts_df['severity_score'] = alerts_df['severity'].map(SEVERITY_MAPPING).fillna(0)
    alerts_df = alerts_df.sort_values(by=['severity_score', 'timestamp'], ascending=[False, False])
    alerts_df = alerts_df.drop(columns=['severity_score'])
    
    alerts_path = os.path.join(data_dir, "alerts.csv")
    alerts_df.to_csv(alerts_path, index=False)
    print(f"Alert engine completed. {len(alerts_df)} unique alerts generated and saved to '{alerts_path}'.")
    
    return alerts_df

if __name__ == "__main__":
    run_alert_engine()
