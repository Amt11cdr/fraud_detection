# Fraud Detection Decision Platform

A real-time fraud detection system that combines **rule-based heuristics and machine learning** to evaluate transactions and make low-latency decisions.

The platform simulates how modern payment systems handle fraud detection: **cheap rule filters handle most traffic, while machine learning is used only for ambiguous transactions.**

---

# System Architecture

```
Transaction Generator
        ↓
Bronze Dataset
        ↓
Rules Engine
        ↓
0 rules → APPROVE
3+ rules → STEP_UP
1–2 rules → ML Model
                ↓
           risk_score
                ↓
         Final Decision
        ↓
Decision Logging
```

This layered approach reduces compute cost and keeps latency low while still allowing deeper analysis of suspicious transactions.

---

# Key Components

## 1. Event Generator

Generates synthetic transaction data to simulate real-world payment activity.

Run:

```
python event_generator/generator.py
```

Output:

```
data/bronze/transactions_v1.csv
```

---

## 2. Rules Engine

The first decision layer applies inexpensive fraud heuristics.

### Rules Implemented

* New country within 24 hours
* Too many failed attempts
* Amount spike relative to user average
* Transaction velocity spike
* New device with high amount

### Routing Policy

```
0 rules triggered → APPROVE
1–2 rules triggered → ML evaluation
3+ rules triggered → STEP_UP
```

Run offline rule evaluation:

```
python rules/apply_rules.py
```

Output:

```
data/silver/transactions_with_rules.csv
```

---

## 3. ML Fraud Risk Model

Borderline transactions are scored using a **Logistic Regression classifier** trained on generated transaction data.

### Model Features

* transaction amount
* new device indicator
* failed attempts (10-minute window)
* transaction velocity
* user average transaction amount

### Model Output

```
risk_score = probability(transaction is fraudulent)
```

### Decision Threshold

```
risk_score < 0.4  → APPROVE
risk_score ≥ 0.4  → STEP_UP
```

---

## 4. Real-Time Scoring API

A FastAPI service exposes the fraud decision engine.

Run the service:

```
uvicorn api.app:app --reload
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

### Example API Response

```json
{
  "transaction_id": "e1866be3-75e8-40dd-a36e-61afdef674c0",
  "decision": "STEP_UP",
  "rule_count": 1,
  "triggered_rules": ["velocity_spike"],
  "risk_score": 0.78,
  "path_taken": "ML_ESCALATION",
  "latency_ms": 3.0
}
```

### Response Fields

* **decision** – final fraud decision
* **rule_count** – number of rules triggered
* **risk_score** – ML fraud probability (null if rules-only path)
* **path_taken** – RULES_ONLY or ML_ESCALATION
* **latency_ms** – request processing latency

---

## 5. Batch API Client

Simulates multiple transactions hitting the fraud scoring API and summarizes system behavior.

Run:

```
python api/test_api_batch.py
```

### Example Results

| Metric             | Value |
| ------------------ | ----- |
| APPROVE            | 17    |
| STEP_UP            | 3     |
| RULES_ONLY path    | 17    |
| ML_ESCALATION path | 3     |

### Average Latency

| Path          | Avg Latency |
| ------------- | ----------- |
| RULES_ONLY    | ~0–1 ms     |
| ML_ESCALATION | ~1–3 ms     |

This demonstrates that:

* the majority of traffic is handled by fast rule evaluation
* ML is invoked only for suspicious edge cases
* the system maintains **sub-100 ms decision latency**

---

## 6. Decision Audit Logging

Every scored transaction is recorded for traceability and monitoring.

Log file:

```
data/audit/api_decisions_log.csv
```

Captured fields include:

* decision
* triggered rules
* ML risk score
* routing path
* latency

---

# Design Rationale

This project uses a **layered fraud detection architecture** rather than applying machine learning to every transaction.

Key design decisions:

* **Rules-first routing** reduces compute cost by filtering obvious cases early.
* **ML scoring is reserved for ambiguous transactions**, improving efficiency.
* **Low-latency decisioning** simulates production payment systems.
* **Audit logging** enables traceability and post-hoc analysis of fraud decisions.

This reflects how real fraud detection platforms balance **accuracy, latency, and infrastructure cost**.

---

# Tech Stack

* Python
* FastAPI
* Pandas
* Scikit-learn
* Uvicorn

---

# Project Structure

```
fraud_detection/
│
├── api/
│   ├── app.py
│   └── test_api_batch.py
│
├── event_generator/
│   └── generator.py
│
├── rules/
│   └── apply_rules.py
│
├── training/
│   └── train_model.py
│
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── audit/
│
└── README.md
```

---

# Author

**Amritansh Tiwari**

