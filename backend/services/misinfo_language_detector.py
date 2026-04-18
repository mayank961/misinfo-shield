MISINFO_PATTERNS = [
    "no evidence",
    "debunked",
    "myth",
    "misleading",
    "false claim",
    "not supported by science",
    "experts say this is misleading",
    "lacks scientific backing",
]

def detect_misinfo_language(text: str):
    t = text.lower()
    for p in MISINFO_PATTERNS:
        if p in t:
            return True
    return False