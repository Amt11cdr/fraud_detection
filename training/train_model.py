import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("data/bronze/transactions_v1.csv")

# Features used for training
features = [
    "amount",
    "is_new_device",
    "failed_attempts_last_10min",
    "transactions_last_10min",
    "user_avg_amount_30d"
]

X = df[features]
y = df["label"]

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000,class_weight="balanced")
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("\nModel Evaluation")
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "training/fraud_model.joblib")

print("\nModel saved to training/fraud_model.joblib")