import sqlite3
from pathlib import Path

DB_PATH = Path("../data/misinfo.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check existing columns
cur.execute("PRAGMA table_info(facts)")
cols = [c[1] for c in cur.fetchall()]

if "embedding" not in cols:
    print("➕ Adding embedding column...")
    cur.execute("ALTER TABLE facts ADD COLUMN embedding BLOB")
    conn.commit()
    print("✅ Column added")
else:
    print("✅ embedding column already exists")

conn.close()