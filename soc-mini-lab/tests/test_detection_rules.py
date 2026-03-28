import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.detection_rules import detect_brute_force, detect_impossible_travel

def test_detect_brute_force():
    now = datetime.now()
    logs = []
    # 5 failed logins for user1
    for i in range(5):
        logs.append([now + timedelta(minutes=i), "user1", "1.1.1.1", "US", "login", "failed", "user"])
    # 1 success after for user1
    logs.append([now + timedelta(minutes=6), "user1", "1.1.1.1", "US", "login", "success", "user"])
    
    df = pd.DataFrame(logs, columns=["timestamp", "username", "source_ip", "country", "event_type", "status", "user_role"])
    
    alerts = detect_brute_force(df)
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "Brute Force Login"
    assert alerts[0]["severity"] == "Critical"
    assert alerts[0]["affected_user"] == "user1"

def test_detect_impossible_travel():
    now = datetime.now()
    logs = [
        [now, "user2", "2.2.2.2", "US", "login", "success", "user"],
        [now + timedelta(hours=2), "user2", "3.3.3.3", "RU", "login", "success", "user"]
    ]
    df = pd.DataFrame(logs, columns=["timestamp", "username", "source_ip", "country", "event_type", "status", "user_role"])
    
    alerts = detect_impossible_travel(df)
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "Impossible Travel"
    assert alerts[0]["severity"] == "High"
    assert alerts[0]["affected_user"] == "user2"
