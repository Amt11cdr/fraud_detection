from engine import evaluate_rules

sample_transaction = {
    "transaction_id": "tx_001",
    "timestamp": "2026-03-06T15:00:00",
    "user_id": "user_1",
    "merchant_id": "merchant_1",
    "amount": 450.0,
    "country": "UK",
    "device_id": "device_99",
    "is_new_device": True,
    "failed_attempts_last_10min": 4,
    "transactions_last_10min": 6,
    "user_avg_amount_30d": 100.0,
    "last_country": "IE"
}

result = evaluate_rules(sample_transaction)
print(result)