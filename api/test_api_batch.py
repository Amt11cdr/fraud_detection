import pandas as pd
import requests

# Load a few rows from the Bronze dataset
df = pd.read_csv("data/bronze/transactions_v1.csv")

# Use only the first 20 rows for now
sample_df = df.head(20)

url = "http://127.0.0.1:8000/score"

results = []

for _, row in sample_df.iterrows():
    payload = row.to_dict()
    # Convert pandas/numpy values into plain Python types
    payload["is_new_device"] = bool(payload["is_new_device"])
    payload["failed_attempts_last_10min"] = int(payload["failed_attempts_last_10min"])
    payload["transactions_last_10min"] = int(payload["transactions_last_10min"])
    payload["amount"] = float(payload["amount"])
    payload["user_avg_amount_30d"] = float(payload["user_avg_amount_30d"])

    response = requests.post(url, json=payload)

    print("Request transaction_id:", payload["transaction_id"])
    print("Status code:", response.status_code)

    try:
        response_json = response.json()
        results.append(response_json)
        print("Response:", response_json)
    except Exception:
        print("Non-JSON response body:")
        print(response.text)
        print("Payload that caused it:")
        print(payload)
        break

    print("-" * 60)

# Summarize results
# Summarize results
results_df = pd.DataFrame(results)

print("\nDecision counts:")
print(results_df["decision"].value_counts())

print("\nPath counts:")
print(results_df["path_taken"].value_counts())

print("\nAverage latency (ms):")
print(results_df["latency_ms"].mean())

print("\nAverage latency by path:")
print(results_df.groupby("path_taken")["latency_ms"].mean())

if "risk_score" in results_df.columns:
    print("\nTransactions that went through ML:")
    ml_rows = results_df[results_df["risk_score"].notna()][
        ["transaction_id", "decision", "risk_score", "path_taken", "latency_ms"]
    ]
    print(ml_rows)
