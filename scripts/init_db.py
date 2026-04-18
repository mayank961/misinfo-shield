import sqlite3

conn = sqlite3.connect("../data/misinfo.db")
cur = conn.cursor()

# Fact DB
cur.execute("""
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim TEXT,
    verdict TEXT,
    explanation TEXT
)
""")

# Cache
cur.execute("""
CREATE TABLE IF NOT EXISTS cache (
    key TEXT PRIMARY KEY,
    response TEXT
)
""")

# Logs
cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input TEXT,
    label TEXT,
    score INTEGER,
    reason TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database initialized")