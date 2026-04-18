import sqlite3
import json
from pathlib import Path

# Use /tmp for HuggingFace Spaces
import os
if os.path.exists("/tmp"):
    DB_PATH = Path("/tmp/misinfo.db")
else:
    DB_PATH = Path(__file__).resolve().parents[2] / "data" / "misinfo.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT NOT NULL,
            verdict TEXT NOT NULL,
            explanation TEXT,
            category TEXT DEFAULT 'general',
            source TEXT DEFAULT 'manual',
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            language TEXT,
            label TEXT,
            score INTEGER,
            reason TEXT,
            fact_checked BOOLEAN,
            fact_confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            label TEXT DEFAULT 'Unverified',
            score INTEGER,
            reviewed BOOLEAN DEFAULT 0,
            verdict TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Auto-load facts from JSON if DB is empty
    count = cursor.execute("SELECT COUNT(*) FROM fact_db").fetchone()[0]
    if count == 0:
        fact_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "fact_db.json"
        if fact_path.exists():
            with open(fact_path, "r", encoding="utf-8") as f:
                facts = json.load(f)
            for fact in facts:
                cursor.execute("""
                    INSERT INTO fact_db (claim, verdict, explanation, category, source)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    fact.get("claim", ""),
                    fact.get("verdict", ""),
                    fact.get("explanation", ""),
                    fact.get("category", "general"),
                    fact.get("source", "manual")
                ))
            conn.commit()
            print(f"✅ Loaded {len(facts)} facts from JSON")

    conn.close()
    print(f"✅ DB ready at: {DB_PATH}")

if __name__ == "__main__":
    init_db()
