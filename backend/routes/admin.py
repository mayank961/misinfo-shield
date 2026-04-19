from fastapi import APIRouter
import sqlite3
from pathlib import Path
from backend.utils.claim_normalizer import normalize_claim_for_api
router = APIRouter()


from backend.config import DB_PATH


def get_conn():
    return sqlite3.connect(str(DB_PATH))
def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ✅ System Stats
@router.get("/admin/stats")
def get_stats():
    conn = get_conn()

    total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    fake = conn.execute("SELECT COUNT(*) FROM logs WHERE label = 'Fake'").fetchone()[0]
    real = conn.execute("SELECT COUNT(*) FROM logs WHERE label = 'Real'").fetchone()[0]
    unverified = conn.execute("SELECT COUNT(*) FROM logs WHERE label = 'Unverified'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM pending_claims WHERE reviewed = 0").fetchone()[0]
    facts = conn.execute("SELECT COUNT(*) FROM fact_db").fetchone()[0]

    conn.close()

    return {
        "total_requests": total,
        "fake": fake,
        "real": real,
        "unverified": unverified,
        "pending_review": pending,
        "facts_in_db": facts
    }


# ✅ Recent Logs
@router.get("/admin/logs")
def get_logs(limit: int = 20):
    conn = get_conn()

    rows = conn.execute("""
        SELECT input, language, label, score, fact_checked, created_at
        FROM logs
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ✅ Pending Claims
@router.get("/admin/pending")
def get_pending():
    conn = get_conn()

    rows = conn.execute("""
        SELECT id, text, label, score, created_at
        FROM pending_claims
        WHERE reviewed = 0
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ✅ Approve a pending claim (mark as Fake or Real)
@router.post("/admin/pending/{claim_id}/approve")
def approve_claim(claim_id: int, data: dict):
    verdict = data.get("verdict")
    explanation = data.get("explanation", "Manually verified")

    if verdict not in ["Fake", "Real"]:
        return {"error": "verdict must be Fake or Real"}

    conn = get_conn()

    row = conn.execute(
        "SELECT text FROM pending_claims WHERE id = ?", (claim_id,)
    ).fetchone()

    if not row:
        conn.close()
        return {"error": "Claim not found"}

    claim_text = row["text"]

    # Add to fact_db
    normalized = normalize_claim_for_api(claim_text)

    conn.execute("""
        INSERT INTO fact_db (claim, normalized_claim, verdict, explanation, category, source)
            VALUES (?, ?, ?, ?, ?, ?)
    """, (claim_text, normalized, verdict, explanation, "pending_review", "manual"))
    # Mark as reviewed
    conn.execute(
        "UPDATE pending_claims SET reviewed = 1, verdict = ? WHERE id = ?",
        (verdict, claim_id)
    )

    conn.commit()
    conn.close()

    # ✅ Clear cache so new fact takes effect immediately
    # ✅ Clear cache so new fact takes effect immediately
    try:
        import os
        cache_db = "/tmp/cache.db" if os.path.exists("/tmp/cache.db") else "database/cache.db"
        cache_conn = sqlite3.connect(cache_db)
        cache_conn.execute("DELETE FROM cache WHERE key LIKE ?", (f"%{claim_text[:20].lower()}%",))
        cache_conn.commit()
        cache_conn.close()
        print(f"🗑️ Cache cleared for: {claim_text[:40]}")
    except Exception as e:
        print(f"⚠️ Cache clear failed: {e}")

# ✅ All Facts in DB
@router.get("/admin/facts")
def get_facts(limit: int = 50):
    conn = get_conn()

    rows = conn.execute("""
        SELECT id, claim, verdict, category, source, created_at
        FROM fact_db
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]