# services/explanation_engine.py

def build_explanation(
    claim: str,
    label: str,
    fact_result: dict,
    external_result: dict,
    confidence: float | None
) -> str:
    """
    Builds a professional, evidence-based explanation
    using actual matched facts or external verdicts.
    """

    # ===== External fact check has highest authority =====
    if external_result.get("matched"):
        verdict = external_result.get("verdict", "No verdict text")
        return (
            f"The claim states: '{claim}'. "
            f"This was checked against trusted external fact-checking sources. "
            f"Verdict from source: {verdict}. "
            f"Therefore, this claim is classified as {label}."
        )

    # ===== Internal semantic fact match =====
    if fact_result.get("matched"):
        matched_claim = fact_result.get("claim", "N/A")
        evidence = fact_result.get("explanation", "No explanation available")
        similarity = fact_result.get("confidence", 0)

        return (
            f"The claim states: '{claim}'. "
            f"Our knowledge base contains a verified fact: '{matched_claim}'. "
            f"Evidence: {evidence}. "
            f"(Semantic similarity score: {similarity:.2f}). "
            f"Based on this evidence, the claim is classified as {label}."
        )

    # ===== Model-only decision =====
    if confidence is not None:
        return (
            f"The claim states: '{claim}'. "
            f"No matching verified fact was found in the database or external sources. "
            f"The AI model analyzed linguistic and contextual patterns "
            f"and predicted this claim as {label} "
            f"with confidence {confidence*100:.1f}%. "
            f"This result is based on learned misinformation patterns."
        )

    # ===== Fallback =====
    return (
        f"The claim states: '{claim}'. "
        f"The system classified this as {label} based on available analysis."
    )