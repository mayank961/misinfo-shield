from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB = PROJECT_ROOT / "backend" / "database" / "facts.db"

print("Using DB:", DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim TEXT,
    verdict TEXT,
    explanation TEXT,
    embedding BLOB
)
""")

conn.commit()
conn.close()

print("✅ facts table created successfully")