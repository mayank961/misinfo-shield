from deep_translator import GoogleTranslator
from langdetect import detect

# Supported languages map
LANGUAGE_MAP = {
    "en": {"name": "English",    "flag": "🇬🇧", "fake": "Fake",       "real": "Real",      "unverified": "Unverified"},
    "hi": {"name": "Hindi",      "flag": "🇮🇳", "fake": "झूठा",       "real": "सच्चा",     "unverified": "अप्रमाणित"},
    "bn": {"name": "Bengali",    "flag": "🇧🇩", "fake": "মিথ্যা",     "real": "সত্য",      "unverified": "অযাচাই"},
    "ta": {"name": "Tamil",      "flag": "🏳️", "fake": "தவறான",      "real": "உண்மை",     "unverified": "சரிபார்க்கப்படவில்லை"},
    "te": {"name": "Telugu",     "flag": "🏳️", "fake": "నకిలీ",      "real": "నిజమైన",    "unverified": "అనిశ్చిత"},
    "mr": {"name": "Marathi",    "flag": "🇮🇳", "fake": "खोटे",       "real": "खरे",       "unverified": "अप्रमाणित"},
    "gu": {"name": "Gujarati",   "flag": "🇮🇳", "fake": "ખોટું",      "real": "સાચું",     "unverified": "અચકાસ્યું"},
    "kn": {"name": "Kannada",    "flag": "🏳️", "fake": "ನಕಲಿ",       "real": "ನಿಜ",       "unverified": "ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ"},
    "ml": {"name": "Malayalam",  "flag": "🏳️", "fake": "വ്യാജം",     "real": "യഥാർത്ഥം", "unverified": "പരിശോധിക്കാത്തത്"},
    "pa": {"name": "Punjabi",    "flag": "🇮🇳", "fake": "ਝੂਠਾ",       "real": "ਸੱਚਾ",     "unverified": "ਅਪ੍ਰਮਾਣਿਤ"},
    "or": {"name": "Odia",       "flag": "🏳️", "fake": "ମିଛ",        "real": "ସତ୍ୟ",     "unverified": "ଅଯାଞ୍ଚିତ"},
    "ur": {"name": "Urdu",       "flag": "🇵🇰", "fake": "جھوٹا",      "real": "سچا",       "unverified": "غیر تصدیق شدہ"},
}

# Languages we support
SUPPORTED_LANGS = set(LANGUAGE_MAP.keys())


def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGS else "en"
    except:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    if source_lang == "en":
        return text
    try:
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except:
        return text


def translate_from_english(text: str, target_lang: str) -> str:
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except:
        return text


def get_label_in_language(label: str, lang: str) -> str:
    lang_data = LANGUAGE_MAP.get(lang, LANGUAGE_MAP["en"])
    label_lower = label.lower()

    if label_lower == "fake":
        return lang_data["fake"]
    elif label_lower == "real":
        return lang_data["real"]
    elif label_lower == "unverified":
        return lang_data["unverified"]
    return label


def get_language_info(lang: str) -> dict:
    return LANGUAGE_MAP.get(lang, LANGUAGE_MAP["en"])