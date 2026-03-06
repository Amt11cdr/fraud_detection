def evaluate_rules(transaction):
    triggered_rules = []

    # Rule 1: New country within 24h
    if transaction["country"] != transaction["last_country"]:
        triggered_rules.append("new_country_24h")

    # Rule 2: Too many failed attempts
    if transaction["failed_attempts_last_10min"] >= 3:
        triggered_rules.append("too_many_failed_attempts")

    # Rule 3: Amount spike
    if transaction["amount"] >= 3 * transaction["user_avg_amount_30d"]:
        triggered_rules.append("amount_spike")

    # Rule 4: Velocity spike
    if transaction["transactions_last_10min"] >= 5:
        triggered_rules.append("velocity_spike")

    # Rule 5: New device + high amount
    if transaction["is_new_device"] and transaction["amount"] >= 2 * transaction["user_avg_amount_30d"]:
        triggered_rules.append("new_device_high_amount")

    rule_count = len(triggered_rules)

    if rule_count == 0:
        decision = "APPROVE"
    elif rule_count <= 2:
        decision = "SEND_TO_ML"
    else:
        decision = "STEP_UP"

    return {
        "triggered_rules": triggered_rules,
        "rule_count": rule_count,
        "decision": decision
    }