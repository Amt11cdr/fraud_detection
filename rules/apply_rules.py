import pandas as pd
from engine import evaluate_rules

# Load the generated transaction data
df = pd.read_csv("data/bronze/transactions_v1.csv")

# Apply the rules engine to each row
results = df.apply(lambda row: evaluate_rules(row.to_dict()), axis=1)

# Convert results into a DataFrame
results_df = pd.DataFrame(results.tolist())

# Combine original data with rule outputs
final_df = pd.concat([df, results_df], axis=1)

# Save the output
output_path = "data/silver/transactions_with_rules.csv"
final_df.to_csv(output_path, index=False)

print(f"Saved enriched transactions to {output_path}")
print(f"\nTotal rows: {len(final_df)}")

print("\nDecision counts:")
print(final_df["decision"].value_counts())

print("\nSample rows:")
print(final_df[["transaction_id", "decision", "rule_count", "triggered_rules"]].head(10))