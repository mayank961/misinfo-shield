def generate_explanation(label: str, text: str, fact_matched: bool):
    
    text_lower = text.lower()

    # Risk keywords
    risky_words = ["breaking", "shocking", "miracle", "urgent"]
    found_words = [word for word in risky_words if word in text_lower]

    # Base explanation
    if label == "Fake":
        explanation = "This content appears to be misleading or false. "
    else:
        explanation = "This content appears to be generally reliable. "

    # Fact-check explanation
    if fact_matched:
        explanation += "A similar claim has been previously fact-checked and found to be incorrect. "

    # Keyword explanation
    if found_words:
        explanation += f"It uses attention-grabbing words like {', '.join(found_words)} which are common in misinformation. "

    # Confidence explanation
    explanation += "Please verify with trusted sources for complete accuracy."

    return explanation