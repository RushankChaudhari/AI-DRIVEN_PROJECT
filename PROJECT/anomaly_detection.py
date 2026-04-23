import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# LOAD DATA
# ==========================================
df = pd.read_csv("healthcare_ops.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# ==========================================
# ANOMALY DETECTION (Isolation Forest)
# ==========================================
features = df[
    ["workload", "response_time_ms", "error_count", "cpu_usage_percent"]
]

model = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = model.fit_predict(features)

print("\n========== ANOMALY DETECTION SUMMARY ==========")
print("Total Records:", len(df))
print("Total Anomalies Detected:", len(df[df["anomaly"] == -1]))

# ==========================================
# SEVERITY CLASSIFICATION
# ==========================================
def classify_severity(row):
    if row["anomaly"] == -1:
        if (
            row["cpu_usage_percent"] > 90
            or row["response_time_ms"] > 1500
            or row["error_count"] > 30
        ):
            return "CRITICAL"
        elif row["cpu_usage_percent"] > 75 or row["response_time_ms"] > 800:
            return "WARNING"
        else:
            return "WARNING"
    else:
        return "HEALTHY"


df["severity"] = df.apply(classify_severity, axis=1)

# ==========================================
# SYSTEM HEALTH SCORE CALCULATION
# ==========================================
print("\n========== SYSTEM HEALTH REPORT ==========")

health_report = []

for system in df["system_name"].unique():
    system_data = df[df["system_name"] == system]

    total_records = len(system_data)
    anomaly_records = len(system_data[system_data["anomaly"] == -1])

    health_score = round(
        ((total_records - anomaly_records) / total_records) * 100, 2
    )

    if health_score > 95:
        status = "STABLE"
    elif health_score >= 85:
        status = "WARNING"
    else:
        status = "CRITICAL"

    print(f"\nSystem: {system}")
    print(f"Total Records: {total_records}")
    print(f"Anomaly Records: {anomaly_records}")
    print(f"Health Score: {health_score}%")
    print(f"Overall Status: {status}")

    health_report.append((system, health_score))

# ==========================================
# HEALTH SCORE BAR CHART
# ==========================================
systems = [item[0] for item in health_report]
scores = [item[1] for item in health_report]

colors = []
for score in scores:
    if score > 95:
        colors.append("green")
    elif score >= 85:
        colors.append("yellow")
    else:
        colors.append("red")

plt.figure(figsize=(10, 6))
plt.bar(systems, scores, color=colors)
plt.xticks(rotation=45)
plt.ylabel("Health Score (%)")
plt.title("System Health Score Overview")
plt.tight_layout()
plt.savefig("system_health_score.png")

print("\nSystem Health Score chart saved as system_health_score.png")

# ==========================================
# SEVERITY HEATMAP
# ==========================================
pivot_table = df.pivot_table(
    index="system_name", columns="date", values="severity", aggfunc="first"
)

severity_mapping = {"HEALTHY": 0, "WARNING": 1, "CRITICAL": 2}

numeric_heatmap = pivot_table.replace(severity_mapping)
numeric_heatmap = numeric_heatmap.fillna(0)
numeric_heatmap = numeric_heatmap.astype(float)

plt.figure(figsize=(15, 6))
sns.heatmap(
    numeric_heatmap,
    cmap=sns.color_palette(["green", "yellow", "red"], as_cmap=True),
    cbar=False,
)

plt.title("Daily System Severity Heatmap")
plt.tight_layout()
plt.savefig("system_severity_heatmap.png")

print("Severity heatmap saved as system_severity_heatmap.png")

# ==========================================
# AI DIAGNOSTIC REPORT (FIXED)
# ==========================================
import random

# Build system_stats dynamically
system_stats = {}

for system in df["system_name"].unique():
    system_data = df[(df["system_name"] == system) & (df["anomaly"] == -1)]

    system_stats[system] = {
        "anomalies": len(system_data),
        "overload": len(system_data[system_data["cpu_usage_percent"] > 90]),
        "performance": len(system_data[system_data["response_time_ms"] > 1500]),
        "failure": len(system_data[system_data["error_count"] > 30]),
    }

# Recommendation pools
server_actions = [
    "Increase server RAM or upgrade CPU capacity.",
    "Enable horizontal scaling across multiple nodes.",
    "Implement load balancing across application servers.",
    "Optimize background processing jobs.",
    "Reduce unnecessary running services.",
    "Enable auto-scaling policies for peak loads.",
]

performance_actions = [
    "Optimize database queries and reduce joins.",
    "Add indexing to frequently accessed tables.",
    "Use caching mechanisms like Redis.",
    "Increase database memory allocation.",
    "Reduce query execution time with optimization.",
    "Tune JVM and application performance parameters.",
]

application_actions = [
    "Inspect application logs for failures.",
    "Fix faulty modules causing repeated errors.",
    "Restart unstable services or APIs.",
    "Deploy latest patches and bug fixes.",
    "Improve exception handling in code.",
    "Monitor API error rates continuously.",
]

network_actions = [
    "Upgrade network bandwidth.",
    "Reduce packet loss using network tuning.",
    "Optimize routing configurations.",
    "Implement traffic throttling.",
    "Monitor network latency patterns.",
]

print("\n========== AI DIAGNOSTIC REPORT ==========\n")

for system in system_stats:
    print(f"System: {system}")
    print(f"Total Anomaly Events: {system_stats[system]['anomalies']}")

    overload = system_stats[system]["overload"]
    performance = system_stats[system]["performance"]
    failure = system_stats[system]["failure"]

    print(f"- {overload} Server Overload events detected")
    print(f"- {performance} Performance Degradation events detected")
    print(f"- {failure} Application Failure events detected")

    print("Recommended Actions:")

    recommendations = []

    if overload > 0:
        recommendations += random.sample(server_actions, 2)

    if performance > 0:
        recommendations += random.sample(performance_actions, 2)

    if failure > 0:
        recommendations += random.sample(application_actions, 2)

    recommendations += random.sample(network_actions, 1)

    recommendations = list(set(recommendations))

    for rec in recommendations:
        print(f"  • {rec}")

    print()

print("Execution Completed Successfully.")
