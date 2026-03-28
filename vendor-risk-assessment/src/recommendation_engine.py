FACTOR_RECOMMENDATIONS = {
    "no_compliance": "Require the vendor to obtain SOC2 Type II or ISO27001 certification before granting access.",
    "admin_access": "Apply the principle of least privilege. Restrict the vendor to the minimum access level required.",
    "write_access": "Implement additional monitoring and audit logging for this vendor's write operations.",
    "high_data_sensitivity": "Enforce end-to-end encryption, strict access controls, and data classification policies.",
    "medium_data_sensitivity": "Apply data handling policies and include data security requirements in the vendor contract.",
    "high_risk_country": "Perform enhanced due diligence. Consult legal to evaluate geopolitical and regulatory risks.",
    "high_business_criticality": "Require a Business Continuity Plan (BCP) and conduct a full third-party security audit.",
    "medium_business_criticality": "Schedule periodic security reviews and ensure vendor has an incident response plan.",
}

GENERAL_HIGH_RISK = "Conduct a full third-party security audit before granting this vendor any access."
GENERAL_CRITICAL = "Escalate to CISO. Do not grant access until all critical risk factors are resolved."


def generate_recommendations(assessment: dict) -> list:
    """
    Given an assessment result, generate a list of recommendations.

    Args:
        assessment: dict from risk_engine.assess_vendor()

    Returns:
        list of recommendation strings
    """
    recommendations = []
    triggered_factors = [f["factor"] for f in assessment.get("triggered_factors", [])]

    for factor in triggered_factors:
        rec = FACTOR_RECOMMENDATIONS.get(factor)
        if rec:
            recommendations.append(rec)

    risk_level = assessment.get("risk_level", "Low")
    if risk_level == "High":
        recommendations.append(GENERAL_HIGH_RISK)
    elif risk_level == "Critical":
        recommendations.append(GENERAL_CRITICAL)

    if not recommendations:
        recommendations.append("No immediate actions required. Continue standard vendor monitoring.")

    return recommendations
