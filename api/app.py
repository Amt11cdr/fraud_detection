from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import pandas as pd
from pathlib import Path
import joblib
import time

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rules.engine import evaluate_rules

app = FastAPI(title="Fraud Detection API")
model = joblib.load("training/fraud_model.joblib")


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
    start_time = time.perf_counter()
    tx_dict = transaction.model_dump()
    result = evaluate_rules(tx_dict)

    risk_score = None
    final_decision = result["decision"]

    # Track which path the transaction takes
    path_taken = "RULES_ONLY"

    # If rules say SEND_TO_ML, call the model
    if result["decision"] == "SEND_TO_ML":

        path_taken = "ML_ESCALATION"
        model_features = [[
            tx_dict["amount"],
            int(tx_dict["is_new_device"]),
            tx_dict["failed_attempts_last_10min"],
            tx_dict["transactions_last_10min"],
            tx_dict["user_avg_amount_30d"]
        ]]

        risk_score = float(model.predict_proba(model_features)[0][1])

        # Simple final decision policy based on ML risk score
        if risk_score < 0.4:
            final_decision = "APPROVE"
        else:
            final_decision = "STEP_UP"

    latency_ms = round((time.perf_counter() - start_time) *1000, 3 )

    response = {
        "transaction_id": transaction.transaction_id,
        "decision": final_decision,
        "rule_count": result["rule_count"],
        "triggered_rules": result["triggered_rules"],
        "risk_score": risk_score,
        "path_taken": path_taken,
        "latency_ms": latency_ms
    }

    # Create audit record
    audit_record = {
        **tx_dict,
        "decision": final_decision,
        "rule_count": result["rule_count"],
        "triggered_rules": str(result["triggered_rules"]),
        "risk_score": risk_score,
        "path_taken": path_taken,
        "latency_ms": latency_ms
    }

    audit_path = Path("data/audit/api_decisions_log.csv")
    audit_df = pd.DataFrame([audit_record])

    if audit_path.exists():
        audit_df.to_csv(audit_path, mode="a", header=False, index=False)
    else:
        audit_df.to_csv(audit_path, index=False)

    print("Scored transaction:", response)
    return response