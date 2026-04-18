import json
import sqlite3
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB = PROJECT_ROOT / "backend" / "database" / "facts.db"
FACT_JSON = PROJECT_ROOT / "data" /"processed"/ "fact_db.json"   # ✅ your facts file

# ===== MODEL =====
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(text: str) -> bytes:
    vec = model.encode(text)
    return np.array(vec).astype(np.float32).tobytes()

# ===== CONNECT DB =====
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ✅ CREATE TABLE (IMPORTANT)
cur.execute("""
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim TEXT,
    verdict TEXT,
    explanation TEXT,
    embedding BLOB
)
""")

# Optional: clear old data to avoid duplicates
cur.execute("DELETE FROM facts")

# ===== LOAD FACTS =====
with open(FACT_JSON, "r", encoding="utf-8") as f:
    facts = json.load(f)

print(f"📦 Loading {len(facts)} facts into DB...")

for fct in facts:
    cur.execute(
        """
        INSERT INTO facts (claim, verdict, explanation, embedding)
        VALUES (?, ?, ?, ?)
        """,
        (
            fct["claim"],
            fct["verdict"],
            fct.get("explanation", ""),
            embed(fct["claim"])
        )
    )

conn.commit()
conn.close()

print("✅ Facts + embeddings loaded into SQLite successfully!")