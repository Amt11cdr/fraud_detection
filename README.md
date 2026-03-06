# Fraud Detection Decision Platform

A real-time fraud scoring system that uses a lightweight rules layer to quickly evaluate transactions and route suspicious ones for deeper analysis.

## Project Overview

This project simulates a real-world fraud detection system architecture. It includes data generation, rule-based decision logic, an API service for scoring transactions, and audit logging of all decisions.

The goal is to demonstrate practical skills in:

- Data engineering
- API-based ML system design
- Decision systems
- Logging and monitoring

## Architecture

Transaction Generator → Bronze Dataset → Rules Engine → FastAPI Scoring Service → Decision Logging

## Components

### 1. Event Generator
Generates synthetic transaction data.

Run:

python event_generator/generator.py


Output:

data/bronze/transactions_v1.csv


### 2. Rules Engine
Applies fraud detection rules to transactions.

Rules include:
- New country within 24 hours
- Too many failed attempts
- Amount spike relative to user average
- Transaction velocity spike
- New device with high amount

Gating policy:

0 rules triggered → APPROVE  
1–2 rules triggered → SEND_TO_ML  
3+ rules triggered → STEP_UP

Run offline rule evaluation:


python rules/apply_rules.py


Output:


data/silver/transactions_with_rules.csv


### 3. Fraud Scoring API

A FastAPI service that scores transactions in real time.

Run the API:


uvicorn api.app:app --reload


Interactive API documentation:


http://127.0.0.1:8000/docs


### 4. Batch API Client

Simulates multiple transactions hitting the fraud scoring service.

Run:


python api/test_api_batch.py


### 5. Decision Audit Logging

Every API decision is logged for traceability.

Output file:


data/audit/api_decisions_log.csv


## Tech Stack

Python  
FastAPI  
Pandas  
Uvicorn  

## Future Improvements

- Add machine learning model for SEND_TO_ML routing
- Implement feature store layer
- Add streaming ingestion
- Add monitoring dashboards

## Author

Amritansh Tiwari
