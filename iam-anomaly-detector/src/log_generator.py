import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

USERS = [f"user{i}" for i in range(1, 30)] + ["admin1", "admin2"]
ROLES = {u: "admin" if u.startswith("admin") else "user" for u in USERS}
COUNTRIES = ["US", "US", "US", "US", "CA", "UK", "IN", "DE"]
DEVICES = ["desktop", "desktop", "mobile"]

def generate_logs():
    print("Generating IAM synthetic logs...")
    start_date = datetime.now() - timedelta(days=14)
    end_date = datetime.now()
    
    logs = []
    current_time = start_date
    
    # Track typical geography/device for users to simulate baseline
    user_baselines = {}
    for u in USERS:
        user_baselines[u] = {
            "country": random.choice(COUNTRIES),
            "device": random.choice(DEVICES)
        }
        
    while current_time < end_date:
        current_time += timedelta(minutes=random.randint(1, 10))
        
        user = random.choice(USERS)
        ip = fake.ipv4()
        role = ROLES[user]
        hour = current_time.hour
        
        # 95% of the time, users log in from their baseline country and device
        if random.random() < 0.95:
            country = user_baselines[user]["country"]
            device = user_baselines[user]["device"]
            status = "success" if random.random() < 0.95 else "failure"
        else:
            country = random.choice(COUNTRIES)
            device = random.choice(DEVICES)
            status = "success" if random.random() < 0.5 else "failure"
            
        logs.append([current_time, user, status, ip, country, device, role, hour])

    # Inject Suspicious Patterns
    
    # 1. Repeated failed login attempts (Brute Force)
    bf_user = "user5"
    bf_time = start_date + timedelta(days=2, hours=10)
    for _ in range(8):
        logs.append([bf_time, bf_user, "failure", fake.ipv4(), "US", "desktop", "user", bf_time.hour])
        bf_time += timedelta(seconds=random.randint(2, 10))
    logs.append([bf_time + timedelta(seconds=5), bf_user, "success", fake.ipv4(), "US", "desktop", "user", bf_time.hour])

    # 2. Login from new country (Impossible Travel)
    it_user = "user12"
    it_time = start_date + timedelta(days=4, hours=12)
    logs.append([it_time, it_user, "success", fake.ipv4(), "US", "desktop", "user", it_time.hour])
    logs.append([it_time + timedelta(minutes=30), it_user, "success", fake.ipv4(), "RU", "desktop", "user", (it_time + timedelta(minutes=30)).hour])

    # 3. Rapid logins from multiple locations
    rl_user = "user18"
    rl_time = start_date + timedelta(days=6, hours=14)
    logs.append([rl_time, rl_user, "success", fake.ipv4(), "US", "mobile", "user", rl_time.hour])
    logs.append([rl_time + timedelta(minutes=5), rl_user, "success", fake.ipv4(), "IN", "mobile", "user", rl_time.hour])
    logs.append([rl_time + timedelta(minutes=10), rl_user, "success", fake.ipv4(), "DE", "desktop", "user", rl_time.hour])

    # 4. Admin access at off-hours
    admin_user = "admin1"
    oh_time = start_date + timedelta(days=8)
    oh_time = oh_time.replace(hour=3, minute=15)
    logs.append([oh_time, admin_user, "success", fake.ipv4(), "US", "desktop", "admin", oh_time.hour])

    # 5. Multiple device switching
    md_user = "user22"
    md_time = start_date + timedelta(days=10, hours=9)
    logs.append([md_time, md_user, "success", fake.ipv4(), "US", "desktop", "user", md_time.hour])
    logs.append([md_time + timedelta(minutes=2), md_user, "success", fake.ipv4(), "US", "mobile", "user", md_time.hour])
    logs.append([md_time + timedelta(minutes=5), md_user, "success", fake.ipv4(), "US", "tablet", "user", md_time.hour])

    # 6. Excessive login frequency
    ef_user = "user25"
    ef_time = start_date + timedelta(days=12, hours=11)
    for _ in range(35):
        logs.append([ef_time, ef_user, "success", fake.ipv4(), "US", "mobile", "user", ef_time.hour])
        ef_time += timedelta(minutes=1)

    logs.sort(key=lambda x: x[0])
    
    df = pd.DataFrame(logs, columns=[
        "timestamp", "user_id", "login_status", "source_ip", 
        "country", "device_type", "user_role", "login_hour"
    ])
    
    data_dir = "/Users/sivas/Documents/GitHub/Cyber_Security/iam-anomaly-detector/data"
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "auth_logs.csv"), index=False)
    
    print(f"Generated {len(df)} authentication logs.")
    print("Saved to data/auth_logs.csv")

if __name__ == "__main__":
    generate_logs()
