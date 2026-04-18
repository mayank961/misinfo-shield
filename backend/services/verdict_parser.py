
def interpret_verdict(verdict: str):
    v = verdict.lower()

    if any(k in v for k in ["false", "misleading", "incorrect", "no evidence",
        "debunked", "myth", "fabricated", "not true",
        "unlikely", "hoax", "scam"]):
        return "Fake"
    if any(k in v for k in ["true", "correct", "accurate"]):
        return "Real"

    return "Unverified"


def extract_source(verdict: str):
    """
    Try to pull source name from external API text.
    Example: 'According to Snopes, this claim is false'
    """
    verdict_lower = verdict.lower()

    sources = [
        "snopes",
        "politifact",
        "factcheck.org",
        "reuters",
        "ap news",
        "bbc",
        "who",
        "cdc"
    ]

    for s in sources:
        if s in verdict_lower:
            return s.title()

    return "Verified source"