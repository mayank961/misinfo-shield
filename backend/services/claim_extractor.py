import re

def extract_claim(text: str) -> str:
    text = text.strip()

    # Remove common filler phrases
    patterns = [
        r"many people say that",
        r"it is believed that",
        r"experts say that",
        r"research shows that",
        r"in my opinion",
        r"according to sources",
        r"it is said that",
        r"some claim that",
        r"reports suggest that"
    ]

    text_lower = text.lower()
    for p in patterns:
        text_lower = re.sub(p, "", text_lower)

    # Keep first sentence (usually the claim)
    sentences = re.split(r'[.!?]', text_lower)
    claim = sentences[0].strip()

    return claim