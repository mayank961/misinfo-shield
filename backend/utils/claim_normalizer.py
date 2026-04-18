import re

def normalize_claim_for_api(text: str) -> str:
    text = text.lower().strip()

    # Remove filler words
    fillers = [
        "many experts believe that",
        "it is believed that",
        "reports suggest that",
        "some people say that",
        "research shows that",
        "it is claimed that",
        "it is said that"
    ]

    for f in fillers:
        text = text.replace(f, "")

    # Remove extra words
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()