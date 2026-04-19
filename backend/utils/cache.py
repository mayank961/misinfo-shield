import sqlite3
import os
import json

# ---------- PATH SETUP (works local + HF) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Detect Hugging Face environment
ON_HF = os.path.exists("/.dockerenv") or os.path.exists("/home/user/app")

if ON_HF:
    DB = "/tmp/misinfo.db"  # only writable place on HF
else:
    DB = os.path.join(PROJECT_ROOT, "misinfo.db")
# ---------------------------------------------------
def init_cache():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_cache(key):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT value FROM cache WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()

    if row:
        import json
        return json.loads(row[0])
    return None

def set_cache(key, value):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    import json
    cur.execute(
        "REPLACE INTO cache (key, value) VALUES (?, ?)",
        (key, json.dumps(value))
    )
    conn.commit()
    conn.close()
