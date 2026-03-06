import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

NUM_ROWS = 500

COUNTRIES = ["IE", "IN", "UK", "DE", "FR"]
USER_IDS = [f"user_{i}" for i in range(1, 51)]
MERCHANT_IDS = [f"merchant_{i}" for i in range(1, 21)]


def generate_transaction():
    user_id = random.choice(USER_IDS)
    merchant_id = random.choice(MERCHANT_IDS)

    user_avg_amount_30d = round(random.uniform(20, 200), 2)
    amount = round(random.uniform(0.5, 2.0) * user_avg_amount_30d, 2)

    last_country = random.choice(COUNTRIES)
    country = last_country

    is_new_device = random.choice([True, False])
    failed_attempts_last_10min = random.randint(0, 2)
    transactions_last_10min = random.randint(0, 4)

    # Inject suspicious behavior sometimes
    if random.random() < 0.10:
        country = random.choice([c for c in COUNTRIES if c != last_country])

    if random.random() < 0.08:
        failed_attempts_last_10min = random.randint(3, 6)

    if random.random() < 0.08:
        transactions_last_10min = random.randint(5, 10)

    if random.random() < 0.07:
        amount = round(random.uniform(3.0, 5.0) * user_avg_amount_30d, 2)

    if random.random() < 0.10:
        is_new_device = True

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 10000))).isoformat(),
        "user_id": user_id,
        "merchant_id": merchant_id,
        "amount": amount,
        "country": country,
        "device_id": f"device_{random.randint(1, 200)}",
        "is_new_device": is_new_device,
        "failed_attempts_last_10min": failed_attempts_last_10min,
        "transactions_last_10min": transactions_last_10min,
        "user_avg_amount_30d": user_avg_amount_30d,
        "last_country": last_country,
    }

    return transaction


def main():
    rows = [generate_transaction() for _ in range(NUM_ROWS)]
    df = pd.DataFrame(rows)

    output_path = "data/bronze/transactions_v1.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} rows to {output_path}")
    print(df.head())


if __name__ == "__main__":
    main()