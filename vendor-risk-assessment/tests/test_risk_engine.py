import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.risk_engine import assess_vendor, classify_risk_level


def test_classify_low():
    assert classify_risk_level(20) == "Low"


def test_classify_medium():
    assert classify_risk_level(50) == "Medium"


def test_classify_high():
    assert classify_risk_level(70) == "High"


def test_classify_critical():
    assert classify_risk_level(90) == "Critical"


def test_critical_vendor():
    vendor = {
        "vendor_name": "BadVendor",
        "country": "RU",
        "data_sensitivity": "High",
        "access_level": "Admin",
        "compliance_status": "None",
        "business_criticality": "High",
    }
    result = assess_vendor(vendor)
    assert result["risk_score"] == 100  # 20+30+40+30+20 = 140, capped
    assert result["risk_level"] == "Critical"
    assert len(result["triggered_factors"]) == 5


def test_low_risk_vendor():
    vendor = {
        "vendor_name": "SafeVendor",
        "country": "US",
        "data_sensitivity": "Low",
        "access_level": "Read",
        "compliance_status": "SOC2",
        "business_criticality": "Low",
    }
    result = assess_vendor(vendor)
    assert result["risk_score"] == 0
    assert result["risk_level"] == "Low"
    assert len(result["triggered_factors"]) == 0
