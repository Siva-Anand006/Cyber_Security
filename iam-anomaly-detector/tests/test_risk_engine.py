import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.risk_engine import calculate_risk_scores
from datetime import datetime


def _alert(rule, severity, user="user1"):
    return {"rule_name": rule, "severity": severity, "user_id": user,
            "timestamp": datetime.now(), "description": "", "recommendation": ""}


def test_critical_brute_force_scores_high():
    alerts = [_alert("brute_force_attempt", "Critical")]
    df = calculate_risk_scores(alerts)
    assert df.loc[0, "risk_score"] == 100  # 40 * 4 = 160, capped at 100
    assert df.loc[0, "risk_level"] == "High"


def test_low_risk_medium_alert():
    alerts = [_alert("off_hours_admin_access", "Medium")]
    df = calculate_risk_scores(alerts)
    assert df.loc[0, "risk_score"] == 40   # 20 * 2 = 40
    assert df.loc[0, "risk_level"] == "Medium"


def test_empty_alerts_returns_empty():
    df = calculate_risk_scores([])
    assert df.empty

