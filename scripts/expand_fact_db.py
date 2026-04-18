import json
from pathlib import Path

MONITOR_PATH = Path("../backend/logs/monitor_log.json")
FACT_DB_PATH = Path("../backend/data/fact_db.json")

def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    monitor_logs = load_json(MONITOR_PATH)
    fact_db = load_json(FACT_DB_PATH)

    existing_claims = {item["claim"] for item in fact_db}

    new_entries = []

    for entry in monitor_logs:
        if entry["label"] == "Unverified" or entry["score"] < 70:
            claim = entry["input"].strip()

            if claim not in existing_claims:
                new_entries.append({
                    "claim": claim,
                    "verdict": "Pending",
                    "explanation": "Auto-added from monitor logs for review"
                })
                existing_claims.add(claim)

    if not new_entries:
        print("✅ No new claims to add.")
        return

    fact_db.extend(new_entries)
    save_json(FACT_DB_PATH, fact_db)

    print(f"✅ Added {len(new_entries)} new claims to fact_db for review.")

if __name__ == "__main__":
    main()