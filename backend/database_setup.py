import sqlite3
from pathlib import Path
import datetime

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "misinfo.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ✅ Create tables (if missing)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT NOT NULL,
        language TEXT,
        label TEXT,
        score INTEGER,
        fact_checked BOOLEAN DEFAULT 0,
        created_at TEXT  -- SQLite TEXT for dates
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pending_claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        label TEXT,
        score INTEGER,
        reviewed BOOLEAN DEFAULT 0,
        verdict TEXT,
        created_at TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_db (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim TEXT UNIQUE NOT NULL,
        verdict TEXT NOT NULL,
        explanation TEXT,
        category TEXT,
        source TEXT,
        created_at TEXT
    )
""")

# ✅ Fix: Add created_at if missing (SQLite-safe way)
cursor.execute("PRAGMA table_info(logs)")
columns = [col[1] for col in cursor.fetchall()]
if 'created_at' not in columns:
    cursor.execute("ALTER TABLE logs ADD COLUMN created_at TEXT")
    # Backfill existing rows
    cursor.execute("UPDATE logs SET created_at = ? WHERE created_at IS NULL", 
                   (datetime.datetime.now().isoformat(),))

# Same for other tables
cursor.execute("PRAGMA table_info(pending_claims)")
if 'created_at' not in [col[1] for col in cursor.fetchall()]:
    cursor.execute("ALTER TABLE pending_claims ADD COLUMN created_at TEXT")

cursor.execute("PRAGMA table_info(fact_db)")
if 'created_at' not in [col[1] for col in cursor.fetchall()]:
    cursor.execute("ALTER TABLE fact_db ADD COLUMN created_at TEXT")

conn.commit()
conn.close()
print("✅ Database fully fixed! All tables ready.")