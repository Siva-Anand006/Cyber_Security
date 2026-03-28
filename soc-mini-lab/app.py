import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SOC Analyst Dashboard", layout="wide")

def load_alerts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alerts_path = os.path.join(base_dir, "data", "alerts.csv")
    if os.path.exists(alerts_path):
        df = pd.read_csv(alerts_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

def load_auth_logs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    auth_path = os.path.join(base_dir, "data", "auth_logs.csv")
    if os.path.exists(auth_path):
        df = pd.read_csv(auth_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

def main():
    st.title("🛡️ SOC Analyst Dashboard")
    st.markdown("Monitor synthetic authentication and API telemetry for suspicious behavior.")
    
    alerts_df = load_alerts()
    auth_df = load_auth_logs()
    
    if alerts_df.empty:
        st.success("No active security alerts. The environment is secure.")
        return
        
    st.header("Executive Summary")
    
    # 1. Total alerts & severity
    col1, col2, col3, col4 = st.columns(4)
    total_alerts = len(alerts_df)
    critical_alerts = len(alerts_df[alerts_df['severity'] == 'Critical'])
    high_alerts = len(alerts_df[alerts_df['severity'] == 'High'])
    medium_alerts = len(alerts_df[alerts_df['severity'] == 'Medium'])
    
    col1.metric("Total Alerts", total_alerts)
    col2.metric("Critical", critical_alerts)
    col3.metric("High", high_alerts)
    col4.metric("Medium", medium_alerts)
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Alerts by Severity")
        severity_counts = alerts_df['severity'].value_counts().reset_index()
        severity_counts.columns = ['Severity', 'Count']
        st.bar_chart(severity_counts, x='Severity', y='Count', color='#ff4b4b')
        
    with col_right:
        st.subheader("Top Suspicious IPs")
        top_ips = alerts_df['source_ip'].value_counts().head(5)
        st.dataframe(top_ips, width='stretch')

    st.markdown("---")
    col_left2, col_right2 = st.columns(2)
    
    with col_left2:
        st.subheader("Users with Most Alerts")
        top_users = alerts_df['affected_user'].value_counts().head(5)
        st.dataframe(top_users, width='stretch')
        
    with col_right2:
        st.subheader("Failed Login Trend")
        if not auth_df.empty:
            failed_logins = auth_df[auth_df['status'] == 'failed']
            if not failed_logins.empty:
                # Resample by day
                failures_by_day = failed_logins.set_index('timestamp').resample('D').size()
                st.line_chart(failures_by_day)
            else:
                st.info("No failed logins detected.")
        else:
            st.info("No authentication data available for trend analysis.")

    st.markdown("---")
    st.subheader("Alert Investigation Table")
    st.dataframe(
        alerts_df[['timestamp', 'severity', 'rule_name', 'affected_user', 'source_ip', 'explanation', 'recommended_action']],
        width='stretch',
        hide_index=True
    )

if __name__ == "__main__":
    main()
