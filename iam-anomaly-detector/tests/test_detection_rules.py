import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.detection_rules import detect_brute_force, detect_impossible_travel, detect_off_hours_admin_access


def make_df(rows):
    return pd.DataFrame(rows, columns=[
        "timestamp", "user_id", "login_status", "source_ip",
        "country", "device_type", "user_role", "login_hour"
    ])


def test_brute_force_critical():
    now = datetime.now()
    rows = [[now + timedelta(minutes=i), "user1", "failure", "1.1.1.1", "US", "desktop", "user", now.hour] for i in range(6)]
    rows.append([now + timedelta(minutes=10), "user1", "success", "1.1.1.1", "US", "desktop", "user", now.hour])
    df = make_df(rows)
    alerts = detect_brute_force(df)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "Critical"
    assert alerts[0]["user_id"] == "user1"


def test_brute_force_high_no_success():
    now = datetime.now()
    rows = [[now + timedelta(minutes=i), "user2", "failure", "2.2.2.2", "US", "desktop", "user", now.hour] for i in range(7)]
    df = make_df(rows)
    alerts = detect_brute_force(df)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "High"


def test_impossible_travel():
    now = datetime.now()
    rows = [
        [now, "user3", "success", "3.3.3.3", "US", "desktop", "user", now.hour],
        [now + timedelta(hours=1), "user3", "success", "4.4.4.4", "RU", "desktop", "user", now.hour],
    ]
    df = make_df(rows)
    alerts = detect_impossible_travel(df)
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "impossible_travel"


def test_off_hours_admin():
    now = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
    rows = [[now, "admin1", "success", "5.5.5.5", "US", "desktop", "admin", now.hour]]
    df = make_df(rows)
    alerts = detect_off_hours_admin_access(df)
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "Medium"

