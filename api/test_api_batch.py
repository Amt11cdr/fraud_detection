import pandas as pd
import requests

# Load a few rows from the Bronze dataset
df = pd.read_csv("data/bronze/transactions_v1.csv")

# Use only the first 10 rows for now
sample_df = df.head(10)

url = "http://127.0.0.1:8000/score"

for _, row in sample_df.iterrows():
    payload = row.to_dict()

    response = requests.post(url, json=payload)

    print("Request transaction_id:", payload["transaction_id"])
    print("Status code:", response.status_code)
    print("Response:", response.json())
    print("-" * 50)