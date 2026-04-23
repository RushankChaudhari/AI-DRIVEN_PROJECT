import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
num_days = 365
anomaly_ratio = 0.03
dirty_ratio = 0.02

start_date = datetime(2025, 1, 1)

systems = [
    "Hospital Management System",
    "Electronic Health Record System",
    "Appointment & Registration System",
    "Hospital Network & Log Systems"
]

data = []

# Generate Normal Data
for day in range(num_days):
    current_date = start_date + timedelta(days=day)

    for system in systems:

        if system == "Hospital Management System":
            workload = random.randint(200, 600)
            response_time = random.randint(150, 350)
            errors = random.randint(0, 5)
            cpu = random.randint(45, 75)

        elif system == "Electronic Health Record System":
            workload = random.randint(300, 800)
            response_time = random.randint(180, 400)
            errors = random.randint(0, 6)
            cpu = random.randint(50, 80)

        elif system == "Appointment & Registration System":
            workload = random.randint(100, 400)
            response_time = random.randint(120, 300)
            errors = random.randint(0, 4)
            cpu = random.randint(40, 70)

        elif system == "Hospital Network & Log Systems":
            workload = random.randint(1000, 3000)
            response_time = random.randint(10, 50)
            errors = random.randint(0, 3)
            cpu = random.randint(30, 65)

        data.append([
            current_date.strftime("%Y-%m-%d"),
            system,
            workload,
            response_time,
            errors,
            cpu
        ])

df = pd.DataFrame(data, columns=[
    "date",
    "system_name",
    "workload",
    "response_time_ms",
    "error_count",
    "cpu_usage_percent"
])

# Inject Anomalies
num_anomalies = int(len(df) * anomaly_ratio)
anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)

for idx in anomaly_indices:
    anomaly_type = random.choice(["OVERLOAD", "APP_FAILURE", "PERFORMANCE"])

    if anomaly_type == "OVERLOAD":
        df.at[idx, "cpu_usage_percent"] = random.randint(95, 100)
        df.at[idx, "response_time_ms"] = random.randint(1500, 2500)
        df.at[idx, "workload"] *= 2

    elif anomaly_type == "APP_FAILURE":
        df.at[idx, "error_count"] = random.randint(40, 60)
        df.at[idx, "response_time_ms"] = random.randint(1000, 2000)

    elif anomaly_type == "PERFORMANCE":
        df.at[idx, "response_time_ms"] = random.randint(2000, 3000)

# Inject Dirty Data
num_dirty = int(len(df) * dirty_ratio)
dirty_indices = np.random.choice(df.index, num_dirty, replace=False)

for idx in dirty_indices:
    dirty_type = random.choice(["INVALID_CPU", "NEGATIVE_ERROR", "NULL_RESPONSE"])

    if dirty_type == "INVALID_CPU":
        df.at[idx, "cpu_usage_percent"] = random.randint(110, 130)

    elif dirty_type == "NEGATIVE_ERROR":
        df.at[idx, "error_count"] = -1

    elif dirty_type == "NULL_RESPONSE":
        df.at[idx, "response_time_ms"] = None

# Save dataset
df.to_csv("healthcare_ops.csv", index=False)

print("====================================")
print("Dataset Generated Successfully")
print("Total Records:", len(df))
print("Anomalies Injected:", num_anomalies)
print("Dirty Records Injected:", num_dirty)
print("====================================")
