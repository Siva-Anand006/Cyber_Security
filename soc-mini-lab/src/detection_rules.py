import pandas as pd

def detect_brute_force(auth_df):
    alerts = []
    # Group by user and check for excessive failed logins
    failed_logins = auth_df[auth_df['status'] == 'failed']
    for user, group in failed_logins.groupby('username'):
        if len(group) >= 5:
            # Check if there is a successful login AFTER the failures
            successes = auth_df[(auth_df['username'] == user) & (auth_df['status'] == 'success')]
            last_failure_time = group['timestamp'].max()
            successful_after = successes[successes['timestamp'] > last_failure_time]
            
            if not successful_after.empty:
                severity = "Critical"
                explanation = f"User {user} had {len(group)} failed logins followed by a successful login."
            else:
                severity = "High"
                explanation = f"User {user} had {len(group)} failed logins."

            alerts.append({
                "rule_name": "Brute Force Login",
                "severity": severity,
                "affected_user": user,
                "source_ip": group['source_ip'].iloc[0],
                "timestamp": group['timestamp'].iloc[-1],
                "explanation": explanation,
                "recommended_action": "Reset user password and block source IP."
            })
    return alerts

def detect_impossible_travel(auth_df):
    alerts = []
    success_logins = auth_df[auth_df['status'] == 'success'].sort_values('timestamp')
    for user, group in success_logins.groupby('username'):
        prev_row = None
        for _, row in group.iterrows():
            if prev_row is not None:
                # Calculate time difference in hours
                time_diff = (row['timestamp'] - prev_row['timestamp']).total_seconds() / 3600.0
                if row['country'] != prev_row['country'] and time_diff < 12:
                    alerts.append({
                        "rule_name": "Impossible Travel",
                        "severity": "High",
                        "affected_user": user,
                        "source_ip": row['source_ip'],
                        "timestamp": row['timestamp'],
                        "explanation": f"Login from {row['country']} just {time_diff:.1f} hours after login from {prev_row['country']}.",
                        "recommended_action": "Investigate user location and enforce MFA."
                    })
            prev_row = row
    return alerts

def detect_off_hours_admin(auth_df):
    alerts = []
    admins = auth_df[(auth_df['user_role'] == 'admin') & (auth_df['status'] == 'success')]
    for _, row in admins.iterrows():
        hour = row['timestamp'].hour
        # Off-hours defined as before 6 AM or after 8 PM
        if hour < 6 or hour > 20: 
            alerts.append({
                "rule_name": "Off-hours Privileged Access",
                "severity": "Medium",
                "affected_user": row['username'],
                "source_ip": row['source_ip'],
                "timestamp": row['timestamp'],
                "explanation": f"Admin access detected during off-hours ({row['timestamp'].strftime('%H:%M')}).",
                "recommended_action": "Verify if the admin was scheduled for maintenance."
            })
    return alerts

def detect_api_burst(api_df):
    alerts = []
    # Identify IPs with excessive API hits (burst)
    for ip, group in api_df.groupby('source_ip'):
        if len(group) >= 50:
            user = group['username'].iloc[0] if not group['username'].empty else "unknown"
            alerts.append({
                "rule_name": "API Burst Activity",
                "severity": "Medium",
                "affected_user": user,
                "source_ip": ip,
                "timestamp": group['timestamp'].max(),
                "explanation": f"Source IP made {len(group)} API requests, indicating potential scraping or enumeration.",
                "recommended_action": "Rate limit the IP and investigate access intent."
            })
    return alerts

def apply_all_rules(auth_df, api_df):
    alerts = []
    if auth_df is not None and not auth_df.empty:
        # Convert timestamp to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(auth_df['timestamp']):
            auth_df['timestamp'] = pd.to_datetime(auth_df['timestamp'])
        alerts.extend(detect_brute_force(auth_df))
        alerts.extend(detect_impossible_travel(auth_df))
        alerts.extend(detect_off_hours_admin(auth_df))
        
    if api_df is not None and not api_df.empty:
        if not pd.api.types.is_datetime64_any_dtype(api_df['timestamp']):
            api_df['timestamp'] = pd.to_datetime(api_df['timestamp'])
        alerts.extend(detect_api_burst(api_df))
        
    return alerts
