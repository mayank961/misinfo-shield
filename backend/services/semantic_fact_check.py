import sqlite3
import torch
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "misinfo.db"

model = SentenceTransformer("all-MiniLM-L6-v2")
SIM_THRESHOLD = 0.72

# Cache
_facts_cache = []
_embeddings_cache = None
_cache_count = 0  # track how many facts were loaded

def load_facts_from_db():
    global _facts_cache, _embeddings_cache, _cache_count

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT claim, verdict, explanation FROM fact_db")
        rows = cursor.fetchall()
        conn.close()

        current_count = len(rows)

        # Only reload if new facts were added
        if current_count != _cache_count:
            _facts_cache = [{"claim": r[0], "verdict": r[1], "explanation": r[2]} for r in rows]
            texts = [f["claim"] for f in _facts_cache]
            _embeddings_cache = model.encode(texts, convert_to_tensor=True) if texts else None
            _cache_count = current_count
            print(f"🔄 Fact DB reloaded: {current_count} facts")

    except Exception as e:
        print(f"⚠️ Could not load facts: {e}")


def semantic_fact_check(text: str):
    # Reload if new facts added
    load_facts_from_db()

    if not _facts_cache or _embeddings_cache is None:
        return {"matched": False}

    query_embedding = model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, _embeddings_cache)[0]
    best_idx = scores.argmax().item()
    best_score = scores[best_idx].item()

    if best_score >= SIM_THRESHOLD:
        matched = _facts_cache[best_idx]
        return {
            "matched": True,
            "claim": matched["claim"],
            "verdict": matched["verdict"],
            "explanation": matched["explanation"],
            "confidence": round(best_score, 2)
        }

    return {"matched": False}


# Initial load at startup
load_facts_from_db()