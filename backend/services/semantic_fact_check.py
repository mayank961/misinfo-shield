import sqlite3
import torch
import os
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Use same path as config
if os.path.exists("/tmp") and os.environ.get("SPACE_ID"):
    DB_PATH = Path("/tmp/misinfo.db")
else:
    DB_PATH = Path(__file__).resolve().parents[2] / "data" / "misinfo.db"

model = SentenceTransformer("all-MiniLM-L6-v2")
SIM_THRESHOLD = 0.72

_facts_cache = []
_embeddings_cache = None
_cache_count = 0

def load_facts_from_db():
    global _facts_cache, _embeddings_cache, _cache_count

    # Wait for DB to be ready (max 10 seconds)
    for attempt in range(10):
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            cursor.execute("SELECT claim, verdict, explanation FROM fact_db")
            rows = cursor.fetchall()
            conn.close()

            current_count = len(rows)
            if current_count != _cache_count:
                _facts_cache = [{"claim": r[0], "verdict": r[1], "explanation": r[2]} for r in rows]
                texts = [f["claim"] for f in _facts_cache]
                _embeddings_cache = model.encode(texts, convert_to_tensor=True) if texts else None
                _cache_count = current_count
                print(f"🔄 Fact DB reloaded: {current_count} facts")
            return

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1}: Could not load facts: {e}")
            time.sleep(1)


def semantic_fact_check(text: str):
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

# Don't load at import time - load on first request
