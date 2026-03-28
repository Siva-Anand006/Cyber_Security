# High-risk countries list (based on common GRC frameworks)
HIGH_RISK_COUNTRIES = {"RU", "CN", "KP", "IR", "BY"}

# Score weights
WEIGHTS = {
    "high_risk_country": 20,
    "no_compliance": 30,
    "partial_compliance": 10,
    "admin_access": 40,
    "write_access": 15,
    "high_data_sensitivity": 30,
    "medium_data_sensitivity": 15,
    "high_business_criticality": 20,
    "medium_business_criticality": 10,
}


def evaluate_country(country: str) -> dict:
    if country in HIGH_RISK_COUNTRIES:
        return {
            "factor": "high_risk_country",
            "score": WEIGHTS["high_risk_country"],
            "explanation": f"Vendor is based in a high-risk jurisdiction ({country})."
        }
    return None


def evaluate_compliance(compliance: str) -> dict:
    if compliance == "None":
        return {
            "factor": "no_compliance",
            "score": WEIGHTS["no_compliance"],
            "explanation": "Vendor has no recognized compliance certification (SOC2 or ISO27001)."
        }
    return None


def evaluate_access_level(access: str) -> dict:
    if access == "Admin":
        return {
            "factor": "admin_access",
            "score": WEIGHTS["admin_access"],
            "explanation": "Vendor has Admin-level access — highest privilege tier."
        }
    if access == "Write":
        return {
            "factor": "write_access",
            "score": WEIGHTS["write_access"],
            "explanation": "Vendor has Write access — can modify or delete data."
        }
    return None


def evaluate_data_sensitivity(sensitivity: str) -> dict:
    if sensitivity == "High":
        return {
            "factor": "high_data_sensitivity",
            "score": WEIGHTS["high_data_sensitivity"],
            "explanation": "Vendor accesses highly sensitive data (e.g., PII, financial, health)."
        }
    if sensitivity == "Medium":
        return {
            "factor": "medium_data_sensitivity",
            "score": WEIGHTS["medium_data_sensitivity"],
            "explanation": "Vendor accesses moderately sensitive data."
        }
    return None


def evaluate_business_criticality(criticality: str) -> dict:
    if criticality == "High":
        return {
            "factor": "high_business_criticality",
            "score": WEIGHTS["high_business_criticality"],
            "explanation": "Vendor supports a business-critical function — outage or breach has major impact."
        }
    if criticality == "Medium":
        return {
            "factor": "medium_business_criticality",
            "score": WEIGHTS["medium_business_criticality"],
            "explanation": "Vendor supports a moderate business function."
        }
    return None


def apply_all_rules(vendor: dict) -> list:
    """Apply all scoring rules to a vendor dict and return a list of triggered factors."""
    results = []
    for func in [
        lambda: evaluate_country(vendor.get("country", "")),
        lambda: evaluate_compliance(vendor.get("compliance_status", "None")),
        lambda: evaluate_access_level(vendor.get("access_level", "Read")),
        lambda: evaluate_data_sensitivity(vendor.get("data_sensitivity", "Low")),
        lambda: evaluate_business_criticality(vendor.get("business_criticality", "Low")),
    ]:
        result = func()
        if result:
            results.append(result)
    return results
