import pandas as pd
import os

def generate_summary():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alerts_path = os.path.join(base_dir, "data", "alerts.csv")
    report_path = os.path.join(base_dir, "docs", "sample_incident_report.md")
    
    if not os.path.exists(alerts_path):
        print("No alerts data found. Generate logs and run alert engine first.")
        return
        
    alerts_df = pd.read_csv(alerts_path)
    if alerts_df.empty:
        print("No alerts to report.")
        return
        
    severity_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
    alerts_df['order'] = alerts_df['severity'].map(severity_order)
    alerts_df = alerts_df.sort_values(by=['order', 'timestamp'])
    
    report_lines = []
    report_lines.append("# Incident Response Summary Report")
    report_lines.append(f"**Date Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("\n## Executive Summary")
    report_lines.append(f"The SOC monitoring pipeline has detected **{len(alerts_df)}** distinct security alerts.")
    
    report_lines.append("\n## Detailed Incident Logs")
    
    count = 1
    for _, row in alerts_df.iterrows():
        report_lines.append(f"### Incident #{count}: {row['rule_name']}")
        report_lines.append(f"- **Severity:** {row['severity']}")
        report_lines.append(f"- **Timestamp:** {row['timestamp']}")
        report_lines.append(f"- **Affected Entity:** {row['affected_user']}")
        report_lines.append(f"- **Source IP:** {row['source_ip']}")
        report_lines.append(f"\n**What Happened & Why it is Suspicious:**")
        report_lines.append(f"The system flagged this activity because: {row['explanation']}")
        report_lines.append(f"\n**Recommended Response:**")
        report_lines.append(f"{row['recommended_action']}\n")
        report_lines.append("---")
        count += 1
        
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Incident report generated successfully at: {report_path}")

if __name__ == "__main__":
    generate_summary()
