import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="IAM Anomaly Detector", layout="wide", page_icon="🔐")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALERTS_PATH = os.path.join(BASE_DIR, "data", "alerts.csv")
AUTH_PATH = os.path.join(BASE_DIR, "data", "auth_logs.csv")

SEVERITY_COLORS = {
    "Critical": "#e74c3c",
    "High": "#e67e22",
    "Medium": "#f1c40f",
    "Low": "#2ecc71",
}


@st.cache_data
def load_alerts():
    if not os.path.exists(ALERTS_PATH):
        return pd.DataFrame()
    df = pd.read_csv(ALERTS_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


@st.cache_data
def load_auth():
    if not os.path.exists(AUTH_PATH):
        return pd.DataFrame()
    df = pd.read_csv(AUTH_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def main():
    st.title("🔐 IAM Anomaly Detector")
    st.markdown("*Identity and Access Monitoring — Analyst Dashboard*")
    st.markdown("---")

    alerts_df = load_alerts()
    auth_df = load_auth()

    if alerts_df.empty:
        st.warning("No alerts found. Run `python src/log_generator.py` and then `python src/alert_engine.py` first.")
        return

    # ── Sidebar filters ───────────────────────────────────────────────────────
    st.sidebar.header("🔍 Filters")
    severity_options = ["All"] + sorted(alerts_df["severity"].unique().tolist())
    selected_severity = st.sidebar.selectbox("Severity", severity_options)

    user_options = ["All"] + sorted(alerts_df["user_id"].unique().tolist())
    selected_user = st.sidebar.selectbox("User", user_options)

    filtered = alerts_df.copy()
    if selected_severity != "All":
        filtered = filtered[filtered["severity"] == selected_severity]
    if selected_user != "All":
        filtered = filtered[filtered["user_id"] == selected_user]

    # ── KPI row ───────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Alerts", len(filtered))
    col2.metric("Critical", len(filtered[filtered["severity"] == "Critical"]))
    col3.metric("High", len(filtered[filtered["severity"] == "High"]))
    col4.metric("Medium", len(filtered[filtered["severity"] == "Medium"]))

    st.markdown("---")

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Alerts by Severity")
        sev_counts = filtered["severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        fig_sev = px.bar(
            sev_counts, x="Severity", y="Count",
            color="Severity",
            color_discrete_map=SEVERITY_COLORS,
            template="plotly_dark"
        )
        fig_sev.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig_sev, use_container_width=True)

    with c2:
        st.subheader("Top Risky Users")
        if "risk_score" in filtered.columns:
            top_users = (
                filtered.groupby("user_id")["risk_score"]
                .max()
                .sort_values(ascending=False)
                .head(8)
                .reset_index()
            )
            top_users.columns = ["User", "Risk Score"]
            fig_users = px.bar(
                top_users, x="Risk Score", y="User",
                orientation="h", color="Risk Score",
                color_continuous_scale="Reds",
                template="plotly_dark"
            )
            fig_users.update_layout(showlegend=False, margin=dict(t=10, b=10), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_users, use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Failed Login Trend")
        if not auth_df.empty:
            fails = auth_df[auth_df["login_status"] == "failure"].copy()
            fails["date"] = fails["timestamp"].dt.date
            daily = fails.groupby("date").size().reset_index(name="Failed Logins")
            fig_trend = px.line(
                daily, x="date", y="Failed Logins",
                markers=True, template="plotly_dark"
            )
            fig_trend.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig_trend, use_container_width=True)

    with c4:
        st.subheader("Suspicious Countries")
        if not auth_df.empty:
            # Highlight non-US logins as suspicious
            suspicious_countries = auth_df[auth_df["country"] != "US"]["country"].value_counts().head(8).reset_index()
            suspicious_countries.columns = ["Country", "Count"]
            fig_geo = px.bar(
                suspicious_countries, x="Country", y="Count",
                color="Count", color_continuous_scale="Oranges",
                template="plotly_dark"
            )
            fig_geo.update_layout(showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig_geo, use_container_width=True)

    # ── Alert table ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader(f"🚨 Alert Investigation Table ({len(filtered)} alerts)")
    display_cols = ["timestamp", "severity", "rule_name", "user_id", "description", "recommendation"]
    if "risk_score" in filtered.columns:
        display_cols += ["risk_score", "risk_level"]
    st.dataframe(
        filtered[display_cols].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()

