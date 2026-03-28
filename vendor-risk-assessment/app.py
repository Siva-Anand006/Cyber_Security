import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.risk_engine import assess_vendor
from src.recommendation_engine import generate_recommendations
from src.utils import load_vendors, score_all_vendors

st.set_page_config(page_title="Vendor Risk Assessment", layout="wide", page_icon="🏢")

RISK_COLORS = {
    "Low": "#2ecc71",
    "Medium": "#f1c40f",
    "High": "#e67e22",
    "Critical": "#e74c3c",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ──────────────────────────────────────────────────────────────────
def risk_badge(level: str) -> str:
    color = RISK_COLORS.get(level, "#999")
    return f'<span style="background:{color};padding:3px 10px;border-radius:12px;color:#000;font-weight:bold;">{level}</span>'


# ── Sidebar nav ──────────────────────────────────────────────────────────────
st.sidebar.title("🏢 Vendor Risk Tool")
st.sidebar.markdown("Third-Party Cyber Risk Assessment")
page = st.sidebar.radio("Navigate", ["🔍 Assess a Vendor", "📊 Portfolio View"])

st.title("🏢 Vendor Risk Assessment Tool")
st.markdown("*Third-Party Cybersecurity Risk Evaluation Platform*")
st.markdown("---")

# ════════════════════════════════════════════════════════════════
# PAGE 1 - VENDOR ASSESSMENT FORM
# ════════════════════════════════════════════════════════════════
if page == "🔍 Assess a Vendor":
    st.subheader("Enter Vendor Details")
    st.markdown("Fill in the fields below to assess a vendor's cybersecurity risk profile.")

    with st.form("vendor_form"):
        col1, col2 = st.columns(2)
        with col1:
            vendor_name = st.text_input("Vendor Name", placeholder="e.g. AlphaTech Solutions")
            country = st.text_input("Country (2-letter code)", placeholder="e.g. US, RU, CN")
            data_sensitivity = st.selectbox("Data Sensitivity", ["Low", "Medium", "High"])
        with col2:
            access_level = st.selectbox("Access Level", ["Read", "Write", "Admin"])
            compliance_status = st.selectbox("Compliance Status", ["None", "SOC2", "ISO27001"])
            business_criticality = st.selectbox("Business Criticality", ["Low", "Medium", "High"])

        submitted = st.form_submit_button("🔎 Assess Risk", use_container_width=True)

    if submitted and vendor_name:
        vendor = {
            "vendor_name": vendor_name,
            "country": country.strip().upper(),
            "data_sensitivity": data_sensitivity,
            "access_level": access_level,
            "compliance_status": compliance_status,
            "business_criticality": business_criticality,
        }
        result = assess_vendor(vendor)
        recommendations = generate_recommendations(result)

        st.markdown("---")
        st.subheader(f"Assessment Report: {vendor_name}")

        # KPI row
        c1, c2, c3 = st.columns(3)
        c1.metric("Risk Score", f"{result['risk_score']} / 100")
        c2.metric("Risk Level", result["risk_level"])
        c3.metric("Risk Factors Triggered", len(result["triggered_factors"]))

        # Risk level visual
        level = result["risk_level"]
        color = RISK_COLORS[level]
        st.markdown(
            f'<div style="background:{color};padding:12px 20px;border-radius:8px;margin:10px 0;">'
            f'<b style="font-size:1.1em;">⚠️ Risk Level: {level}</b></div>',
            unsafe_allow_html=True
        )

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["risk_score"],
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 30], "color": "#d5f5e3"},
                    {"range": [30, 60], "color": "#fef9e7"},
                    {"range": [60, 80], "color": "#fdebd0"},
                    {"range": [80, 100], "color": "#f9ebea"},
                ],
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Triggered factors
        st.subheader("🔴 Triggered Risk Factors")
        if result["triggered_factors"]:
            for f in result["triggered_factors"]:
                st.markdown(f"- **+{f['score']} pts** — {f['explanation']}")
        else:
            st.success("No risk factors triggered.")

        # Recommendations
        st.subheader("✅ Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")

    elif submitted:
        st.warning("Please enter a vendor name.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 - PORTFOLIO VIEW
# ════════════════════════════════════════════════════════════════
else:
    vendors_path = os.path.join(BASE_DIR, "data", "sample_vendors.csv")
    if not os.path.exists(vendors_path):
        st.error("sample_vendors.csv not found in data/")
        st.stop()

    df = load_vendors()
    scored = score_all_vendors(df)

    # ── Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Vendors", len(scored))
    c2.metric("Critical", len(scored[scored["risk_level"] == "Critical"]))
    c3.metric("High", len(scored[scored["risk_level"] == "High"]))
    c4.metric("Medium", len(scored[scored["risk_level"] == "Medium"]))
    st.markdown("---")

    col_left, col_right = st.columns(2)

    # ── Bar chart: risk score per vendor (top 15)
    with col_left:
        st.subheader("Risk Score by Vendor")
        top = scored.head(15)
        fig_bar = px.bar(
            top,
            x="risk_score", y="vendor_name",
            orientation="h",
            color="risk_level",
            color_discrete_map=RISK_COLORS,
            template="plotly_dark",
            labels={"risk_score": "Risk Score", "vendor_name": "Vendor", "risk_level": "Risk Level"},
        )
        fig_bar.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=10, b=10), showlegend=True)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Pie chart: risk level distribution
    with col_right:
        st.subheader("Risk Level Distribution")
        dist = scored["risk_level"].value_counts().reset_index()
        dist.columns = ["Risk Level", "Count"]
        fig_pie = px.pie(
            dist,
            names="Risk Level", values="Count",
            color="Risk Level",
            color_discrete_map=RISK_COLORS,
            template="plotly_dark",
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Heatmap: Access Level vs. Data Sensitivity
    st.subheader("Risk Heatmap — Access Level × Data Sensitivity")
    heatmap_data = scored.groupby(["access_level", "data_sensitivity"])["risk_score"].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="access_level", columns="data_sensitivity", values="risk_score").fillna(0)
    fig_heat = px.imshow(
        heatmap_pivot,
        text_auto=True,
        color_continuous_scale="Reds",
        template="plotly_dark",
        labels={"color": "Avg Risk Score"},
    )
    fig_heat.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Vendor portfolio table
    st.markdown("---")
    st.subheader("📋 Vendor Portfolio Table")

    # Sidebar filter
    levels = st.multiselect("Filter by Risk Level", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"])
    filtered = scored[scored["risk_level"].isin(levels)]

    display_cols = ["vendor_name", "country", "access_level", "compliance_status", "data_sensitivity", "business_criticality", "risk_score", "risk_level"]
    st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True, hide_index=True)
