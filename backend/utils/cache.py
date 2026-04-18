import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE_DIR, "database", "cache.db")

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