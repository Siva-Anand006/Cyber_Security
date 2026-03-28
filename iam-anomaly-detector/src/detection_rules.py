import pandas as pd


def detect_brute_force(df):
    """Detect > 5 failed logins followed by a success for the same user."""
    alerts = []
    failures = df[df["login_status"] == "failure"]
    for user, group in failures.groupby("user_id"):
        if len(group) >= 5:
            last_fail = group["timestamp"].max()
            success_after = df[
                (df["user_id"] == user) &
                (df["login_status"] == "success") &
                (df["timestamp"] > last_fail)
            ]
            if not success_after.empty:
                severity = "Critical"
                description = f"{user} had {len(group)} failed logins followed by a successful one."
            else:
                severity = "High"
                description = f"{user} had {len(group)} failed logins with no success."

            alerts.append({
                "rule_name": "brute_force_attempt",
                "severity": severity,
                "user_id": user,
                "timestamp": group["timestamp"].iloc[-1],
                "description": description,
                "recommendation": "Reset credentials and block source IP immediately."
            })
    return alerts


def detect_impossible_travel(df):
    """Detect same user logging in from different countries within 2 hours."""
    alerts = []
    successes = df[df["login_status"] == "success"].sort_values("timestamp")
    for user, group in successes.groupby("user_id"):
        rows = group.reset_index(drop=True)
        for i in range(1, len(rows)):
            prev = rows.iloc[i - 1]
            curr = rows.iloc[i]
            diff_hours = (curr["timestamp"] - prev["timestamp"]).total_seconds() / 3600
            if curr["country"] != prev["country"] and diff_hours < 2:
                alerts.append({
                    "rule_name": "impossible_travel",
                    "severity": "High",
                    "user_id": user,
                    "timestamp": curr["timestamp"],
                    "description": (
                        f"{user} logged in from {prev['country']} and then {curr['country']} "
                        f"within {diff_hours:.1f} hours."
                    ),
                    "recommendation": "Verify user identity and enforce MFA."
                })
    return alerts


def detect_off_hours_admin_access(df):
    """Detect admin logins outside 8 AM – 8 PM."""
    alerts = []
    admins = df[(df["user_role"] == "admin") & (df["login_status"] == "success")]
    for _, row in admins.iterrows():
        hour = row["login_hour"]
        if hour < 8 or hour >= 20:
            alerts.append({
                "rule_name": "off_hours_admin_access",
                "severity": "Medium",
                "user_id": row["user_id"],
                "timestamp": row["timestamp"],
                "description": f"Admin {row['user_id']} logged in at {hour:02d}:00 outside business hours.",
                "recommendation": "Confirm if maintenance was scheduled; review access logs."
            })
    return alerts


def detect_excessive_login_frequency(df):
    """Detect users with > 25 logins within a rolling 1-hour window."""
    alerts = []
    df_sorted = df.sort_values("timestamp")
    for user, group in df_sorted.groupby("user_id"):
        group = group.set_index("timestamp").sort_index()
        # count any numeric column over a rolling 1-hour window
        rolling_counts = group["login_hour"].rolling("1h").count()
        peak = rolling_counts.max()
        if peak > 25:
            peak_time = rolling_counts.idxmax()
            alerts.append({
                "rule_name": "excessive_login_frequency",
                "severity": "Medium",
                "user_id": user,
                "timestamp": peak_time,
                "description": f"{user} made {int(peak)} login attempts within a 1-hour window.",
                "recommendation": "Investigate automation or credential stuffing. Apply rate limiting."
            })
    return alerts


def apply_all_rules(df):
    """Run all rules and return combined list of alerts."""
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    alerts = []
    alerts.extend(detect_brute_force(df))
    alerts.extend(detect_impossible_travel(df))
    alerts.extend(detect_off_hours_admin_access(df))
    alerts.extend(detect_excessive_login_frequency(df))
    return alerts

