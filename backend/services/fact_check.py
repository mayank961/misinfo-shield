import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load database
with open("../data/processed/fact_db.json", "r", encoding="utf-8") as f:
    fact_db = json.load(f)

# Create embeddings
claims = [item["claim"] for item in fact_db]
claim_embeddings = model.encode(claims)

def check_fact(text: str):
    text_embedding = model.encode([text])[0]

    similarities = []

    for i, emb in enumerate(claim_embeddings):
        sim = np.dot(text_embedding, emb) / (
            np.linalg.norm(text_embedding) * np.linalg.norm(emb)
        )
        similarities.append(sim)

    best_match_idx = int(np.argmax(similarities))
    best_score = similarities[best_match_idx]

    # Threshold
    THRESHOLD = 0.75
    if best_score > THRESHOLD:
        matched = fact_db[best_match_idx]
        return {
            "matched": True,
            "verdict": matched["verdict"],
            "explanation": matched["explanation"],
            "confidence": float(best_score)
        }

    return {"matched": False}