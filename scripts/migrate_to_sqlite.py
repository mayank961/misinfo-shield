import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "misinfo.db"

print(f"📁 DB Path: {DB_PATH}")

def get_conn():
    return sqlite3.connect(str(DB_PATH))

def migrate_fact_db():
    path = BASE_DIR / "data" / "processed" / "fact_db.json"
    if not path.exists():
        print(f"⚠️ fact_db.json not found at {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        facts = json.load(f)

    conn = get_conn()
    cursor = conn.cursor()
    count = 0

    for fact in facts:
        try:
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
            count += 1
        except Exception as e:
            print(f"❌ Error inserting fact: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Migrated {count} facts to SQLite")

def migrate_pending_claims():
    path = BASE_DIR / "data" / "pending_claims.json"
    if not path.exists():
        print(f"⚠️ pending_claims.json not found — skipping (no pending claims yet)")
        return

    with open(path, "r", encoding="utf-8") as f:
        try:
            claims = json.load(f)
        except:
            claims = []

    conn = get_conn()
    cursor = conn.cursor()
    count = 0

    for claim in claims:
        cursor.execute("""
            INSERT INTO pending_claims (text, label, score)
            VALUES (?, ?, ?)
        """, (
            claim.get("text", ""),
            claim.get("label", "Unverified"),
            claim.get("score", 0)
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ Migrated {count} pending claims to SQLite")

if __name__ == "__main__":
    migrate_fact_db()
    migrate_pending_claims()
    print("\n🎉 Migration complete!")
    
    # Verify
    conn = get_conn()
    facts_count = conn.execute("SELECT COUNT(*) FROM fact_db").fetchone()[0]
    pending_count = conn.execute("SELECT COUNT(*) FROM pending_claims").fetchone()[0]
    conn.close()
    
    print(f"📊 Facts in DB: {facts_count}")
    print(f"📊 Pending claims in DB: {pending_count}")