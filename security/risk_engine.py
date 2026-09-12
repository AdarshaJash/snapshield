WEIGHTS = {
    "credential_request": 25,
    "urgency": 15,
    "suspicious_url": 25,
    "brand_impersonation": 20,
    "payment_request": 20,
}

def score_indicators(indicators):
    score = min(sum(WEIGHTS.get(k, 0) for k, v in indicators.items() if v), 100)
    level = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
    return {"score": score, "level": level}
