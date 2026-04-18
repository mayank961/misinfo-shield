import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "misinfo.db"

def log_request(result: dict):
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO logs (input, language, label, score, reason, fact_checked, fact_confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            result.get("input", ""),
            result.get("language", "en"),
            result.get("label", ""),
            result.get("score", 0),
            result.get("reason", ""),
            result.get("fact_checked", False),
            result.get("fact_confidence", None)
        ))

        if result.get("label") == "Unverified" or result.get("score", 100) < 70:
            cursor.execute("""
                INSERT INTO pending_claims (text, label, score)
                VALUES (?, ?, ?)
            """, (
                result.get("input", ""),
                result.get("label", ""),
                result.get("score", 0)
            ))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"⚠️ Logging error: {e}")