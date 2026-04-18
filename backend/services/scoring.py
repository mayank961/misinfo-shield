def calculate_score(model_score: int, fact_matched: bool, text: str):
    
    # Normalize model score (0–100)
    model_weight = model_score * 0.6

    # Fact check boost
    if fact_matched:
        fact_weight = 30
    else:
        fact_weight = 0

    # Keyword risk
    risky_words = ["breaking", "shocking", "miracle", "urgent"]
    keyword_weight = 0

    for word in risky_words:
        if word in text.lower():
            keyword_weight = 10
            break

    final_score = int(model_weight + fact_weight + keyword_weight)

    # Clamp score
    final_score = max(0, min(100, final_score))

    return final_score