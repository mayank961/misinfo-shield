from fastapi import APIRouter
from services.model import predict
from services.scoring import calculate_score
from services.explanation import generate_explanation
from services.semantic_fact_check import semantic_fact_check
from services.external_fact import check_external_fact
from services.verdict_parser import interpret_verdict
from services.misinfo_language_detector import detect_misinfo_language
from services.explanation_engine import build_explanation
from services.credibility_engine import adjust_score
from services.translator import (
    detect_language,
    translate_to_english,
    translate_from_english,
    get_label_in_language,
    get_language_info
)
from utils.logger import log_request
from utils.cache import get_cache, set_cache
from services.claim_extractor import extract_claim
from utils.claim_normalizer import normalize_claim_for_api

router = APIRouter()


@router.post("/detect")
def detect(data: dict):
    text = data.get("text")

    # ❌ Empty input
    if not text or not text.strip():
        return {"error": "Input text is empty"}

    # ✅ Detect language FIRST (before extraction)
    lang = detect_language(text)
    lang_info = get_language_info(lang)
    original_text = text

    # ✅ Translate to English for AI processing
    if lang != "en":
        text = translate_to_english(text, lang)

    # ✅ Claim extraction (on English text)
    text = extract_claim(text)

    # ✅ Cache key
    cache_key = f"{original_text.strip().lower()}_{lang}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return dict(cached_result)

    # ✅ Misinformation language detection
    if detect_misinfo_language(text):
        label_translated = get_label_in_language("Fake", lang)
        reason_en = "The sentence contains strong misinformation indicators (debunked/myth/misleading/no evidence)."
        reason = translate_from_english(reason_en, lang) if lang != "en" else reason_en

        result = {
            "input": original_text,
            "language": lang,
            "language_name": lang_info["name"],
            "flag": lang_info["flag"],
            "label": label_translated,
            "label_en": "Fake",
            "score": 92,
            "reason": reason,
            "fact_checked": False,
            "fact_confidence": None
        }
        log_request(result)
        set_cache(cache_key, result)
        return result

    # ✅ Semantic fact check
    fact_result = semantic_fact_check(text)

    # ✅ External fact check
    external_result = {"matched": False}
    if not fact_result.get("matched"):
        clean_claim = normalize_claim_for_api(text)
        external_result = check_external_fact(clean_claim)

    # ✅ Decision Logic
    confidence = None

    if external_result.get("matched"):
        label_en = interpret_verdict(external_result.get("verdict", ""))
        score = calculate_score(95, True, text)

    elif fact_result.get("matched"):
        label_en = fact_result.get("verdict")
        score = calculate_score(92, True, text)

    else:
        label_en, base_score, confidence = predict(text)
        if confidence < 0.60:
            label_en = "Unverified"
            score = int(confidence * 100)
        else:
            score = calculate_score(base_score, False, text)

    # ✅ Credibility scoring
    score = adjust_score(score, fact_result, external_result, confidence)

    # ✅ Build explanation in English first
    reason_core = build_explanation(
        claim=text,
        label=label_en,
        fact_result=fact_result,
        external_result=external_result,
        confidence=confidence
    )

    extra_reason = generate_explanation(
        label_en,
        text,
        fact_result.get("matched") or external_result.get("matched")
    )

    reason_en = reason_core + " " + extra_reason

    # ✅ Translate label and reason to user's language
    label_translated = get_label_in_language(label_en, lang)
    reason = translate_from_english(reason_en, lang) if lang != "en" else reason_en

    # ✅ Final response
    result = {
        "input": original_text,
        "language": lang,
        "language_name": lang_info["name"],
        "flag": lang_info["flag"],
        "label": label_translated,
        "label_en": label_en,
        "score": score,
        "reason": reason,
        "fact_checked": fact_result.get("matched") or external_result.get("matched"),
        "fact_confidence": fact_result.get("confidence", None)
    }

    log_request(result)
    set_cache(cache_key, result)

    return result