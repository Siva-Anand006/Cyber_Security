import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scoring_rules import evaluate_country, evaluate_compliance, evaluate_access_level, evaluate_data_sensitivity


def test_high_risk_country_triggers():
    result = evaluate_country("RU")
    assert result is not None
    assert result["factor"] == "high_risk_country"
    assert result["score"] == 20


def test_safe_country_no_trigger():
    result = evaluate_country("US")
    assert result is None


def test_no_compliance_triggers():
    result = evaluate_compliance("None")
    assert result is not None
    assert result["factor"] == "no_compliance"
    assert result["score"] == 30


def test_soc2_no_trigger():
    result = evaluate_compliance("SOC2")
    assert result is None


def test_admin_access_triggers():
    result = evaluate_access_level("Admin")
    assert result is not None
    assert result["score"] == 40


def test_read_access_no_trigger():
    result = evaluate_access_level("Read")
    assert result is None


def test_high_sensitivity_triggers():
    result = evaluate_data_sensitivity("High")
    assert result is not None
    assert result["score"] == 30


def test_low_sensitivity_no_trigger():
    result = evaluate_data_sensitivity("Low")
    assert result is None
