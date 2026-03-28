import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scoring_rules import apply_all_rules


def classify_risk_level(score: int) -> str:
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    elif score <= 80:
        return "High"
    else:
        return "Critical"


def assess_vendor(vendor: dict) -> dict:
    """
    Run all scoring rules against a vendor and return a structured assessment.

    Args:
        vendor: dict with keys: vendor_name, country, data_sensitivity,
                access_level, compliance_status, business_criticality

    Returns:
        dict with risk_score, risk_level, triggered_factors
    """
    triggered = apply_all_rules(vendor)
    raw_score = sum(f["score"] for f in triggered)
    score = min(raw_score, 100)
    level = classify_risk_level(score)

    return {
        "vendor_name": vendor.get("vendor_name", "Unknown"),
        "risk_score": score,
        "risk_level": level,
        "triggered_factors": triggered,
    }
