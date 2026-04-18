import sqlite3
from pathlib import Path

# D:\misinfo-shield\data\misinfo.db
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "misinfo.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # creates data\ if missing
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
    conn.close()
    print(f"✅ DB created at: {DB_PATH}")

if __name__ == "__main__":
    init_db()