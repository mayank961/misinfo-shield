import requests

API_KEY = "AIzaSyB67Fl9uXCDGXzEuJkwgpe2VmG__4Ob0Vc"

def check_external_fact(text: str):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    params = {
        "query": text,
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        claims = data.get("claims")

        if claims:
            top_claim = claims[0]
            claim_text = top_claim.get("text", "")

            review = top_claim.get("claimReview", [])[0]
            verdict = review.get("textualRating", "")

            return {
                "matched": True,
                "claim": claim_text,
                "verdict": verdict
            }

    except Exception as e:
        print("API error:", e)

    return {"matched": False}