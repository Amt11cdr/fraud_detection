from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import pandas as pd
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rules.engine import evaluate_rules

app = FastAPI(title="Fraud Detection API")


class TransactionRequest(BaseModel):
    transaction_id: str
    timestamp: str
    user_id: str
    merchant_id: str
    amount: float
    country: str
    device_id: str
    is_new_device: bool
    failed_attempts_last_10min: int
    transactions_last_10min: int
    user_avg_amount_30d: float
    last_country: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/score")
def score_transaction(transaction: TransactionRequest):
    tx_dict = transaction.model_dump()
    result = evaluate_rules(tx_dict)

    response = {
        "transaction_id": transaction.transaction_id,
        "decision": result["decision"],
        "rule_count": result["rule_count"],
        "triggered_rules": result["triggered_rules"]
    }

    # Create audit record
    audit_record = {
        **tx_dict,
        "decision": result["decision"],
        "rule_count": result["rule_count"],
        "triggered_rules": str(result["triggered_rules"])
    }

    audit_path = Path("data/audit/api_decisions_log.csv")
    audit_df = pd.DataFrame([audit_record])

    if audit_path.exists():
        audit_df.to_csv(audit_path, mode="a", header=False, index=False)
    else:
        audit_df.to_csv(audit_path, index=False)

    print("Scored transaction:", response)
    return response