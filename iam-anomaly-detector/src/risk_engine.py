import pandas as pd

# Weight assigned to each rule type when computing a risk score (max 100)
RULE_WEIGHTS = {
    "brute_force_attempt": 40,
    "impossible_travel": 30,
    "off_hours_admin_access": 20,
    "excessive_login_frequency": 15,
}

SEVERITY_WEIGHTS = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def calculate_risk_scores(alerts):
    """
    Given a list of alert dicts, compute a risk score (0-100) per user.
    Returns a DataFrame with: user_id, risk_score, risk_level
    """
    if not alerts:
        return pd.DataFrame(columns=["user_id", "risk_score", "risk_level"])

    alerts_df = pd.DataFrame(alerts)
    user_scores = {}

    for user, group in alerts_df.groupby("user_id"):
        score = 0
        for _, row in group.iterrows():
            rule_weight = RULE_WEIGHTS.get(row["rule_name"], 10)
            sev_multiplier = SEVERITY_WEIGHTS.get(row["severity"], 1)
            score += rule_weight * sev_multiplier

        # Cap score at 100
        score = min(score, 100)
        user_scores[user] = score

    risk_df = pd.DataFrame(user_scores.items(), columns=["user_id", "risk_score"])
    risk_df["risk_level"] = risk_df["risk_score"].apply(
        lambda s: "High" if s >= 60 else ("Medium" if s >= 30 else "Low")
    )
    return risk_df.sort_values("risk_score", ascending=False).reset_index(drop=True)

