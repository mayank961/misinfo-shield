def adjust_score(score, fact_result, external_result, confidence):
    # External evidence credibility
    if external_result.get("matched"):
        verdict = external_result.get("verdict", "").lower()

        strong_sources = ["who", "cdc", "reuters", "bbc", "ap news"]
        weak_sources = ["blog", "unknown"]

        if any(s in verdict for s in strong_sources):
            return min(score + 3, 99)

        if any(s in verdict for s in weak_sources):
            return max(score - 3, 85)

        return min(score + 1, 97)

    # Internal fact similarity based boost
    if fact_result.get("matched"):
        sim = fact_result.get("confidence", 0)

        if sim > 0.90:
            return min(score + 2, 96)
        if sim > 0.80:
            return score
        return max(score - 2, 85)

    # Model only case
    if confidence is not None:
        if confidence > 0.85:
            return min(score + 2, 95)
        if confidence < 0.60:
            return max(score - 5, 50)

    return score