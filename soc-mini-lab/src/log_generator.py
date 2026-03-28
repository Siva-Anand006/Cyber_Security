import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()

USERS = [f"user{i}" for i in range(1, 20)] + ["admin1", "admin2"]
COUNTRIES = ["US", "US", "US", "CA", "UK", "IN", "DE"]
ENDPOINTS = ["/api/v1/data", "/api/v1/status", "/api/v1/users", "/api/v1/settings", "/auth/login"]
ROLES = {u: "admin" if u.startswith("admin") else "user" for u in USERS}

def generate_auth_logs(start_date, num_days=7):
    logs = []
    current_time = start_date
    end_date = start_date + timedelta(days=num_days)
    
    while current_time < end_date:
        current_time += timedelta(minutes=random.randint(1, 15))
        
        user = random.choice(USERS)
        ip = fake.ipv4()
        country = random.choices(COUNTRIES, weights=[70, 10, 5, 5, 5, 3, 2])[0]
        role = ROLES[user]
        
        # Normal behavior
        if random.random() < 0.9:
            logs.append([current_time, user, ip, country, "login", "success", role])
        else:
            logs.append([current_time, user, ip, country, "login", "failed", role])
            
    # --- Anomalous Scenarios ---
    
    # 1. Brute Force Login
    bf_user = "user3"
    bf_ip = fake.ipv4()
    bf_time = start_date + timedelta(days=1, hours=10)
    for _ in range(15):
        logs.append([bf_time, bf_user, bf_ip, "US", "login", "failed", "user"])
        bf_time += timedelta(seconds=random.randint(2, 10))
    # Finally succeed
    logs.append([bf_time + timedelta(seconds=5), bf_user, bf_ip, "US", "login", "success", "user"])

    # 2. Impossible Travel
    it_user = "user5"
    it_time = start_date + timedelta(days=2, hours=14)
    logs.append([it_time, it_user, fake.ipv4(), "US", "login", "success", "user"])
    logs.append([it_time + timedelta(minutes=5), it_user, fake.ipv4(), "RU", "login", "success", "user"])

    # 3. Off-hours Admin Access
    admin_user = "admin1"
    oh_time = (start_date + timedelta(days=3)).replace(hour=3, minute=15)
    logs.append([oh_time, admin_user, fake.ipv4(), "US", "login", "success", "admin"])

    # Sort
    logs.sort(key=lambda x: x[0])
    return pd.DataFrame(logs, columns=["timestamp", "username", "source_ip", "country", "event_type", "status", "user_role"])

def generate_api_logs(auth_df):
    logs = []
    
    for _, row in auth_df.iterrows():
        if row["status"] == "success":
            for _ in range(random.randint(1, 5)):
                api_time = row["timestamp"] + timedelta(seconds=random.randint(1, 60))
                endpoint = random.choice(ENDPOINTS)
                status_code = 200 if random.random() > 0.05 else 403
                logs.append([api_time, row["username"], row["source_ip"], endpoint, status_code])
                
    # 4. API Burst Access
    burst_user = "user7"
    burst_ip = fake.ipv4()
    if not auth_df.empty:
        burst_time = auth_df.iloc[0]["timestamp"] + timedelta(days=4)
    else:
        burst_time = datetime.now()
        
    for _ in range(100):
        logs.append([burst_time, burst_user, burst_ip, "/api/v1/data", 200])
        burst_time += timedelta(milliseconds=random.randint(50, 200))

    logs.sort(key=lambda x: x[0])
    return pd.DataFrame(logs, columns=["timestamp", "username", "source_ip", "endpoint", "response_code"])

def generate_logs():
    print("Generating synthetic SOC logs...")
    start_date = datetime.now() - timedelta(days=7)
    
    auth_df = generate_auth_logs(start_date)
    api_df = generate_api_logs(auth_df)
    
    data_dir = "/Users/sivas/Documents/GitHub/Cyber_Security/soc-mini-lab/data"
    os.makedirs(data_dir, exist_ok=True)
    
    auth_df.to_csv(os.path.join(data_dir, "auth_logs.csv"), index=False)
    api_df.to_csv(os.path.join(data_dir, "api_logs.csv"), index=False)
    
    print(f"Generated {len(auth_df)} authentication events.")
    print(f"Generated {len(api_df)} API events.")
    print("Files saved to data directory.")

if __name__ == "__main__":
    generate_logs()
