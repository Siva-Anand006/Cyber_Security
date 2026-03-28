import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.alert_engine import SEVERITY_MAPPING

def test_severity_mapping():
    assert SEVERITY_MAPPING["Critical"] == 4
    assert SEVERITY_MAPPING["High"] == 3
    assert SEVERITY_MAPPING["Medium"] == 2
    assert SEVERITY_MAPPING["Low"] == 1
