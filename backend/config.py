from pathlib import Path
import os

if os.path.exists("/tmp") and os.environ.get("SPACE_ID"):
    DB_PATH = Path("/tmp/misinfo.db")
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    DB_PATH = DATA_DIR / "misinfo.db"
